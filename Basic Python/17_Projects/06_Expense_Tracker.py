"""A persistent personal-finance expense and income tracker.

Uses Decimal for all monetary arithmetic to avoid floating-point
rounding errors.
"""

from __future__ import annotations

import json
import logging
import uuid
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from enum import Enum
from pathlib import Path

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

DEFAULT_STORAGE_PATH = Path.cwd() / "data" / "expenses.json"


class TransactionError(Exception):
    """Base exception for transaction-related failures."""


class TransactionNotFoundError(TransactionError):
    """Raised when a requested transaction ID does not exist."""


class InvalidTransactionDataError(TransactionError):
    """Raised when transaction input data fails validation."""


class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"


@dataclass(slots=True)
class Transaction:
    """Represents a single financial transaction."""

    type: TransactionType
    amount: Decimal
    category: str
    description: str
    txn_date: str
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type.value,
            "amount": str(self.amount),
            "category": self.category,
            "description": self.description,
            "txn_date": self.txn_date,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Transaction:
        return cls(
            id=data["id"],
            type=TransactionType(data["type"]),
            amount=Decimal(data["amount"]),
            category=data["category"],
            description=data.get("description", ""),
            txn_date=data["txn_date"],
        )


class ExpenseRepository:
    """Handles JSON persistence for transactions."""

    def __init__(self, storage_path: Path = DEFAULT_STORAGE_PATH) -> None:
        self._storage_path = storage_path
        self._storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not self._storage_path.exists():
            self._write_all([])

    def load_all(self) -> list[Transaction]:
        try:
            raw = self._storage_path.read_text(encoding="utf-8")
            payload = json.loads(raw) if raw.strip() else []
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Failed to load transactions (%s); starting with empty list.", exc)
            return []
        return [Transaction.from_dict(item) for item in payload]

    def save_all(self, transactions: list[Transaction]) -> None:
        self._write_all([t.to_dict() for t in transactions])

    def _write_all(self, payload: list[dict]) -> None:
        tmp_path = self._storage_path.with_suffix(".tmp")
        tmp_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        tmp_path.replace(self._storage_path)


class ExpenseTrackerService:
    """Business logic for managing transactions, independent of any UI."""

    def __init__(self, repository: ExpenseRepository) -> None:
        self._repository = repository
        self._transactions: dict[str, Transaction] = {
            t.id: t for t in repository.load_all()
        }

    def add_transaction(
        self,
        txn_type: TransactionType,
        amount: str,
        category: str,
        description: str = "",
        txn_date: str | None = None,
    ) -> Transaction:
        parsed_amount = self._parse_amount(amount)
        category = category.strip()
        if not category:
            raise InvalidTransactionDataError("Category cannot be empty.")
        txn_date = txn_date or date.today().isoformat()
        self._validate_date(txn_date)

        transaction = Transaction(
            type=txn_type, amount=parsed_amount, category=category,
            description=description.strip(), txn_date=txn_date,
        )
        self._transactions[transaction.id] = transaction
        self._persist()
        return transaction

    def delete_transaction(self, txn_id: str) -> None:
        self._get_or_raise(txn_id)
        del self._transactions[txn_id]
        self._persist()

    def calculate_balance(self) -> Decimal:
        balance = Decimal("0")
        for txn in self._transactions.values():
            balance += txn.amount if txn.type is TransactionType.INCOME else -txn.amount
        return balance

    def category_summary(self) -> dict[str, Decimal]:
        summary: dict[str, Decimal] = {}
        for txn in self._transactions.values():
            if txn.type is TransactionType.EXPENSE:
                summary[txn.category] = summary.get(txn.category, Decimal("0")) + txn.amount
        return dict(sorted(summary.items(), key=lambda kv: kv[1], reverse=True))

    def monthly_summary(self, year: int, month: int) -> dict[str, Decimal]:
        prefix = f"{year:04d}-{month:02d}"
        income = expenses = Decimal("0")
        for txn in self._transactions.values():
            if not txn.txn_date.startswith(prefix):
                continue
            if txn.type is TransactionType.INCOME:
                income += txn.amount
            else:
                expenses += txn.amount
        return {"income": income, "expenses": expenses, "net": income - expenses}

    def filter_by_date_range(self, start: str, end: str) -> list[Transaction]:
        self._validate_date(start)
        self._validate_date(end)
        return [t for t in self._transactions.values() if start <= t.txn_date <= end]

    def list_transactions(self) -> list[Transaction]:
        return sorted(self._transactions.values(), key=lambda t: t.txn_date, reverse=True)

    def _get_or_raise(self, txn_id: str) -> Transaction:
        txn = self._transactions.get(txn_id)
        if txn is None:
            raise TransactionNotFoundError(f"No transaction found with ID '{txn_id}'.")
        return txn

    @staticmethod
    def _parse_amount(raw: str) -> Decimal:
        try:
            amount = Decimal(raw)
        except InvalidOperation as exc:
            raise InvalidTransactionDataError(f"Invalid amount: '{raw}'.") from exc
        if amount <= 0:
            raise InvalidTransactionDataError("Amount must be greater than zero.")
        return amount

    @staticmethod
    def _validate_date(value: str) -> None:
        try:
            date.fromisoformat(value)
        except ValueError as exc:
            raise InvalidTransactionDataError(
                f"Invalid date '{value}'. Use YYYY-MM-DD format."
            ) from exc

    def _persist(self) -> None:
        self._repository.save_all(list(self._transactions.values()))


def _print_menu() -> None:
    print("\n================================")
    print("        EXPENSE TRACKER")
    print("================================")
    print("1. Add income")
    print("2. Add expense")
    print("3. List transactions")
    print("4. Show balance")
    print("5. Category summary")
    print("6. Monthly summary")
    print("7. Delete transaction")
    print("0. Exit")


def _handle_add(service: ExpenseTrackerService, txn_type: TransactionType) -> None:
    amount = input("Amount: ").strip()
    category = input("Category: ").strip()
    description = input("Description (optional): ").strip()
    txn_date = input("Date YYYY-MM-DD (blank = today): ").strip() or None
    try:
        txn = service.add_transaction(txn_type, amount, category, description, txn_date)
        print(f"Recorded transaction {txn.id}.")
    except TransactionError as exc:
        print(f"Error: {exc}")


def _handle_list(service: ExpenseTrackerService) -> None:
    transactions = service.list_transactions()
    if not transactions:
        print("No transactions found.")
        return
    for txn in transactions:
        sign = "+" if txn.type is TransactionType.INCOME else "-"
        print(f"[{txn.id}] {txn.txn_date} | {sign}{txn.amount} | {txn.category} | {txn.description}")


def _handle_balance(service: ExpenseTrackerService) -> None:
    print(f"Current balance: {service.calculate_balance()}")


def _handle_category_summary(service: ExpenseTrackerService) -> None:
    summary = service.category_summary()
    if not summary:
        print("No expenses recorded.")
        return
    for category, total in summary.items():
        print(f"{category}: {total}")


def _handle_monthly_summary(service: ExpenseTrackerService) -> None:
    try:
        year = int(input("Year (YYYY): ").strip())
        month = int(input("Month (1-12): ").strip())
    except ValueError:
        print("Invalid year or month.")
        return
    summary = service.monthly_summary(year, month)
    print(f"Income: {summary['income']} | Expenses: {summary['expenses']} | Net: {summary['net']}")


def _handle_delete(service: ExpenseTrackerService) -> None:
    txn_id = input("Transaction ID: ").strip()
    try:
        service.delete_transaction(txn_id)
        print("Transaction deleted.")
    except TransactionError as exc:
        print(f"Error: {exc}")


def main() -> None:
    """Entry point for the interactive expense tracker CLI."""
    service = ExpenseTrackerService(ExpenseRepository())

    while True:
        _print_menu()
        choice = input("Select an option: ").strip()
        if choice == "0":
            print("Goodbye.")
            break
        elif choice == "1":
            _handle_add(service, TransactionType.INCOME)
        elif choice == "2":
            _handle_add(service, TransactionType.EXPENSE)
        elif choice == "3":
            _handle_list(service)
        elif choice == "4":
            _handle_balance(service)
        elif choice == "5":
            _handle_category_summary(service)
        elif choice == "6":
            _handle_monthly_summary(service)
        elif choice == "7":
            _handle_delete(service)
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
