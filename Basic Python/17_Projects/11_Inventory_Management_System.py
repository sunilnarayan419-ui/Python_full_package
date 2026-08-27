"""A professional inventory-management system backed by SQLite.

Tracks products, stock movements, and valuations using Decimal for all
monetary calculations.
"""

from __future__ import annotations

import logging
import sqlite3
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterator

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

DEFAULT_DB_PATH = Path.cwd() / "data" / "inventory.db"


class InventoryError(Exception):
    """Base exception for inventory-related failures."""


class ProductNotFoundError(InventoryError):
    """Raised when a requested product does not exist."""


class InsufficientStockError(InventoryError):
    """Raised when a stock-out would drive quantity negative."""


class InvalidInventoryDataError(InventoryError):
    """Raised when input data fails validation."""


class DuplicateSkuError(InventoryError):
    """Raised when a product with the same SKU already exists."""


@dataclass(slots=True)
class Product:
    sku: str
    name: str
    category: str
    quantity: int
    unit_price: Decimal
    reorder_level: int


@dataclass(slots=True)
class StockTransaction:
    id: str
    sku: str
    change: int
    reason: str
    timestamp: str


class InventoryRepository:
    """Handles SQLite persistence and schema management for inventory."""

    def __init__(self, db_path: Path = DEFAULT_DB_PATH) -> None:
        self._db_path = db_path
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_schema()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self._db_path)
        connection.execute("PRAGMA foreign_keys = ON")
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    def _initialize_schema(self) -> None:
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    sku TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price TEXT NOT NULL,
                    reorder_level INTEGER NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS stock_transactions (
                    id TEXT PRIMARY KEY,
                    sku TEXT NOT NULL REFERENCES products(sku),
                    change INTEGER NOT NULL,
                    reason TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_txn_sku ON stock_transactions(sku)")

    def add_product(self, product: Product) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO products (sku, name, category, quantity, unit_price, reorder_level) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (product.sku, product.name, product.category, product.quantity,
                 str(product.unit_price), product.reorder_level),
            )

    def get_product(self, sku: str) -> Product | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM products WHERE sku = ?", (sku,)).fetchone()
            return self._row_to_product(row) if row else None

    def update_quantity(self, sku: str, quantity: int) -> None:
        with self._connect() as conn:
            conn.execute("UPDATE products SET quantity = ? WHERE sku = ?", (quantity, sku))

    def list_products(self) -> list[Product]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM products ORDER BY name").fetchall()
            return [self._row_to_product(r) for r in rows]

    def search_products(self, query: str) -> list[Product]:
        with self._connect() as conn:
            like = f"%{query}%"
            rows = conn.execute(
                "SELECT * FROM products WHERE name LIKE ? OR category LIKE ? OR sku LIKE ? "
                "ORDER BY name",
                (like, like, like),
            ).fetchall()
            return [self._row_to_product(r) for r in rows]

    def add_transaction(self, transaction: StockTransaction) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO stock_transactions (id, sku, change, reason, timestamp) "
                "VALUES (?, ?, ?, ?, ?)",
                (transaction.id, transaction.sku, transaction.change,
                 transaction.reason, transaction.timestamp),
            )

    def list_transactions(self, sku: str) -> list[StockTransaction]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM stock_transactions WHERE sku = ? ORDER BY timestamp DESC", (sku,)
            ).fetchall()
            return [
                StockTransaction(r["id"], r["sku"], r["change"], r["reason"], r["timestamp"])
                for r in rows
            ]

    @staticmethod
    def _row_to_product(row: sqlite3.Row) -> Product:
        return Product(row["sku"], row["name"], row["category"], row["quantity"],
                        Decimal(row["unit_price"]), row["reorder_level"])


class InventoryService:
    """Business rules for inventory management, independent of persistence."""

    def __init__(self, repository: InventoryRepository) -> None:
        self._repository = repository

    def register_product(
        self, sku: str, name: str, category: str, unit_price: str,
        initial_quantity: int = 0, reorder_level: int = 0,
    ) -> Product:
        sku, name, category = sku.strip(), name.strip(), category.strip()
        if not sku or not name or not category:
            raise InvalidInventoryDataError("SKU, name, and category are required.")
        if initial_quantity < 0 or reorder_level < 0:
            raise InvalidInventoryDataError("Quantity and reorder level cannot be negative.")

        price = self._parse_price(unit_price)
        product = Product(sku=sku, name=name, category=category, quantity=initial_quantity,
                           unit_price=price, reorder_level=reorder_level)
        try:
            self._repository.add_product(product)
        except sqlite3.IntegrityError as exc:
            raise DuplicateSkuError(f"A product with SKU '{sku}' already exists.") from exc
        return product

    def stock_in(self, sku: str, quantity: int, reason: str = "Restock") -> Product:
        if quantity <= 0:
            raise InvalidInventoryDataError("Stock-in quantity must be positive.")
        product = self._get_or_raise(sku)
        new_quantity = product.quantity + quantity
        self._repository.update_quantity(sku, new_quantity)
        self._record_transaction(sku, quantity, reason)
        product.quantity = new_quantity
        return product

    def stock_out(self, sku: str, quantity: int, reason: str = "Sale") -> Product:
        if quantity <= 0:
            raise InvalidInventoryDataError("Stock-out quantity must be positive.")
        product = self._get_or_raise(sku)
        if product.quantity < quantity:
            raise InsufficientStockError(
                f"Cannot remove {quantity} units; only {product.quantity} in stock."
            )
        new_quantity = product.quantity - quantity
        self._repository.update_quantity(sku, new_quantity)
        self._record_transaction(sku, -quantity, reason)
        product.quantity = new_quantity
        return product

    def low_stock_products(self) -> list[Product]:
        return [p for p in self._repository.list_products() if p.quantity <= p.reorder_level]

    def total_valuation(self) -> Decimal:
        return sum(
            (p.unit_price * p.quantity for p in self._repository.list_products()),
            Decimal("0"),
        )

    def search(self, query: str) -> list[Product]:
        return self._repository.search_products(query)

    def list_products(self) -> list[Product]:
        return self._repository.list_products()

    def transaction_history(self, sku: str) -> list[StockTransaction]:
        self._get_or_raise(sku)
        return self._repository.list_transactions(sku)

    def _get_or_raise(self, sku: str) -> Product:
        product = self._repository.get_product(sku)
        if product is None:
            raise ProductNotFoundError(f"No product found with SKU '{sku}'.")
        return product

    def _record_transaction(self, sku: str, change: int, reason: str) -> None:
        transaction = StockTransaction(
            id=uuid.uuid4().hex[:8], sku=sku, change=change, reason=reason,
            timestamp=datetime.now().isoformat(timespec="seconds"),
        )
        self._repository.add_transaction(transaction)

    @staticmethod
    def _parse_price(raw: str) -> Decimal:
        try:
            price = Decimal(raw)
        except InvalidOperation as exc:
            raise InvalidInventoryDataError(f"Invalid unit price: '{raw}'.") from exc
        if price < 0:
            raise InvalidInventoryDataError("Unit price cannot be negative.")
        return price


def _print_menu() -> None:
    print("\n================================")
    print("   INVENTORY MANAGEMENT SYSTEM")
    print("================================")
    print("1. Register product")
    print("2. Stock in")
    print("3. Stock out")
    print("4. List products")
    print("5. Search products")
    print("6. Low-stock report")
    print("7. Total valuation")
    print("8. Transaction history")
    print("0. Exit")


def _read_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Please enter a whole number.")


def _handle_register(service: InventoryService) -> None:
    sku = input("SKU: ").strip()
    name = input("Name: ").strip()
    category = input("Category: ").strip()
    price = input("Unit price: ").strip()
    quantity = _read_int("Initial quantity: ")
    reorder_level = _read_int("Reorder level: ")
    try:
        product = service.register_product(sku, name, category, price, quantity, reorder_level)
        print(f"Registered product {product.sku}.")
    except InventoryError as exc:
        print(f"Error: {exc}")


def _handle_stock_in(service: InventoryService) -> None:
    sku = input("SKU: ").strip()
    quantity = _read_int("Quantity to add: ")
    reason = input("Reason (optional) [Restock]: ").strip() or "Restock"
    try:
        product = service.stock_in(sku, quantity, reason)
        print(f"New quantity for {product.sku}: {product.quantity}")
    except InventoryError as exc:
        print(f"Error: {exc}")


def _handle_stock_out(service: InventoryService) -> None:
    sku = input("SKU: ").strip()
    quantity = _read_int("Quantity to remove: ")
    reason = input("Reason (optional) [Sale]: ").strip() or "Sale"
    try:
        product = service.stock_out(sku, quantity, reason)
        print(f"New quantity for {product.sku}: {product.quantity}")
    except InventoryError as exc:
        print(f"Error: {exc}")


def _print_product(product: Product) -> None:
    print(f"[{product.sku}] {product.name} | {product.category} | "
          f"qty={product.quantity} | price={product.unit_price} | reorder@{product.reorder_level}")


def _handle_list(service: InventoryService) -> None:
    products = service.list_products()
    if not products:
        print("No products found.")
        return
    for product in products:
        _print_product(product)


def _handle_search(service: InventoryService) -> None:
    query = input("Search query: ").strip()
    results = service.search(query)
    if not results:
        print("No matching products.")
        return
    for product in results:
        _print_product(product)


def _handle_low_stock(service: InventoryService) -> None:
    products = service.low_stock_products()
    if not products:
        print("No products are below their reorder level.")
        return
    for product in products:
        _print_product(product)


def _handle_valuation(service: InventoryService) -> None:
    print(f"Total inventory valuation: {service.total_valuation()}")


def _handle_history(service: InventoryService) -> None:
    sku = input("SKU: ").strip()
    try:
        transactions = service.transaction_history(sku)
    except InventoryError as exc:
        print(f"Error: {exc}")
        return
    if not transactions:
        print("No transaction history.")
        return
    for txn in transactions:
        print(f"[{txn.timestamp}] {txn.change:+d} ({txn.reason})")


def main() -> None:
    """Entry point for the interactive inventory management CLI."""
    service = InventoryService(InventoryRepository())
    actions = {
        "1": _handle_register,
        "2": _handle_stock_in,
        "3": _handle_stock_out,
        "4": _handle_list,
        "5": _handle_search,
        "6": _handle_low_stock,
        "7": _handle_valuation,
        "8": _handle_history,
    }

    while True:
        _print_menu()
        choice = input("Select an option: ").strip()
        if choice == "0":
            print("Goodbye.")
            break
        action = actions.get(choice)
        if action is None:
            print("Invalid choice.")
            continue
        action(service)


if __name__ == "__main__":
    main()
