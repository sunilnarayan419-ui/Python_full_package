"""A professional educational banking simulation backed by SQLite.

This is a software-engineering exercise, not a real banking system.
No authentication credentials are stored. All monetary values use
Decimal, and transaction integrity is enforced at the database level.
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

DEFAULT_DB_PATH = Path.cwd() / "data" / "bank.db"


class BankingError(Exception):
    """Base exception for banking-related failures."""


class CustomerNotFoundError(BankingError):
    """Raised when a requested customer does not exist."""


class AccountNotFoundError(BankingError):
    """Raised when a requested account does not exist."""


class InsufficientFundsError(BankingError):
    """Raised when a withdrawal exceeds the available balance."""


class InvalidBankingDataError(BankingError):
    """Raised when input data fails validation."""


class DuplicateAccountError(BankingError):
    """Raised when an account identifier collision occurs."""


@dataclass(slots=True)
class Customer:
    id: str
    name: str
    email: str


@dataclass(slots=True)
class Account:
    id: str
    customer_id: str
    account_type: str
    balance: Decimal


@dataclass(slots=True)
class BankTransaction:
    id: str
    account_id: str
    type: str
    amount: Decimal
    timestamp: str
    note: str


class BankRepository:
    """Handles SQLite persistence and schema management for the bank."""

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
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _initialize_schema(self) -> None:
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    id TEXT PRIMARY KEY,
                    customer_id TEXT NOT NULL REFERENCES customers(id),
                    account_type TEXT NOT NULL,
                    balance TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id TEXT PRIMARY KEY,
                    account_id TEXT NOT NULL REFERENCES accounts(id),
                    type TEXT NOT NULL,
                    amount TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    note TEXT NOT NULL
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_accounts_customer ON accounts(customer_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_txn_account ON transactions(account_id)")

    def add_customer(self, customer: Customer) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO customers (id, name, email) VALUES (?, ?, ?)",
                (customer.id, customer.name, customer.email),
            )

    def get_customer(self, customer_id: str) -> Customer | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM customers WHERE id = ?", (customer_id,)).fetchone()
            return Customer(row["id"], row["name"], row["email"]) if row else None

    def add_account(self, account: Account) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO accounts (id, customer_id, account_type, balance) VALUES (?, ?, ?, ?)",
                (account.id, account.customer_id, account.account_type, str(account.balance)),
            )

    def get_account(self, account_id: str) -> Account | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM accounts WHERE id = ?", (account_id,)).fetchone()
            return self._row_to_account(row) if row else None

    def update_balance(self, account_id: str, new_balance: Decimal) -> None:
        with self._connect() as conn:
            conn.execute(
                "UPDATE accounts SET balance = ? WHERE id = ?", (str(new_balance), account_id)
            )

    def add_transaction(self, transaction: BankTransaction) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO transactions (id, account_id, type, amount, timestamp, note) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (transaction.id, transaction.account_id, transaction.type,
                 str(transaction.amount), transaction.timestamp, transaction.note),
            )

    def list_transactions(self, account_id: str) -> list[BankTransaction]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM transactions WHERE account_id = ? ORDER BY timestamp DESC",
                (account_id,),
            ).fetchall()
            return [
                BankTransaction(r["id"], r["account_id"], r["type"], Decimal(r["amount"]),
                                 r["timestamp"], r["note"])
                for r in rows
            ]

    def list_accounts_for_customer(self, customer_id: str) -> list[Account]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM accounts WHERE customer_id = ?", (customer_id,)
            ).fetchall()
            return [self._row_to_account(r) for r in rows]

    def execute_atomic(self, operation) -> None:
        """Run `operation(connection)` inside a single transaction."""
        with self._connect() as conn:
            operation(conn)

    @staticmethod
    def _row_to_account(row: sqlite3.Row) -> Account:
        return Account(row["id"], row["customer_id"], row["account_type"], Decimal(row["balance"]))


class BankingService:
    """Business rules for the bank, independent of persistence details."""

    def __init__(self, repository: BankRepository) -> None:
        self._repository = repository

    def register_customer(self, name: str, email: str) -> Customer:
        name, email = name.strip(), email.strip().lower()
        if not name or not email:
            raise InvalidBankingDataError("Name and email are required.")
        customer = Customer(id=uuid.uuid4().hex[:8], name=name, email=email)
        try:
            self._repository.add_customer(customer)
        except sqlite3.IntegrityError as exc:
            raise InvalidBankingDataError(f"A customer with email '{email}' already exists.") from exc
        return customer

    def open_account(self, customer_id: str, account_type: str, opening_balance: str = "0") -> Account:
        if self._repository.get_customer(customer_id) is None:
            raise CustomerNotFoundError(f"No customer found with ID '{customer_id}'.")
        account_type = account_type.strip().lower()
        if account_type not in ("checking", "savings"):
            raise InvalidBankingDataError("Account type must be 'checking' or 'savings'.")

        balance = self._parse_amount(opening_balance, allow_zero=True)
        account = Account(id=uuid.uuid4().hex[:10], customer_id=customer_id,
                           account_type=account_type, balance=balance)
        try:
            self._repository.add_account(account)
        except sqlite3.IntegrityError as exc:
            raise DuplicateAccountError("Account ID collision; please retry.") from exc
        return account

    def deposit(self, account_id: str, amount: str) -> Account:
        account = self._get_account_or_raise(account_id)
        parsed = self._parse_amount(amount)
        new_balance = account.balance + parsed
        self._repository.update_balance(account_id, new_balance)
        self._record_transaction(account_id, "deposit", parsed, "Cash deposit")
        account.balance = new_balance
        return account

    def withdraw(self, account_id: str, amount: str) -> Account:
        account = self._get_account_or_raise(account_id)
        parsed = self._parse_amount(amount)
        if parsed > account.balance:
            raise InsufficientFundsError(
                f"Insufficient funds: balance is {account.balance}, requested {parsed}."
            )
        new_balance = account.balance - parsed
        self._repository.update_balance(account_id, new_balance)
        self._record_transaction(account_id, "withdrawal", parsed, "Cash withdrawal")
        account.balance = new_balance
        return account

    def transfer(self, source_account_id: str, target_account_id: str, amount: str) -> None:
        source = self._get_account_or_raise(source_account_id)
        target = self._get_account_or_raise(target_account_id)
        parsed = self._parse_amount(amount)
        if parsed > source.balance:
            raise InsufficientFundsError(
                f"Insufficient funds: balance is {source.balance}, requested {parsed}."
            )

        new_source_balance = source.balance - parsed
        new_target_balance = target.balance + parsed

        def _apply(conn: sqlite3.Connection) -> None:
            conn.execute("UPDATE accounts SET balance = ? WHERE id = ?",
                         (str(new_source_balance), source_account_id))
            conn.execute("UPDATE accounts SET balance = ? WHERE id = ?",
                         (str(new_target_balance), target_account_id))
            timestamp = datetime.now().isoformat(timespec="seconds")
            conn.execute(
                "INSERT INTO transactions (id, account_id, type, amount, timestamp, note) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (uuid.uuid4().hex[:8], source_account_id, "transfer_out", str(parsed),
                 timestamp, f"Transfer to {target_account_id}"),
            )
            conn.execute(
                "INSERT INTO transactions (id, account_id, type, amount, timestamp, note) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (uuid.uuid4().hex[:8], target_account_id, "transfer_in", str(parsed),
                 timestamp, f"Transfer from {source_account_id}"),
            )

        self._repository.execute_atomic(_apply)

    def balance_inquiry(self, account_id: str) -> Decimal:
        return self._get_account_or_raise(account_id).balance

    def transaction_history(self, account_id: str) -> list[BankTransaction]:
        self._get_account_or_raise(account_id)
        return self._repository.list_transactions(account_id)

    def customer_accounts(self, customer_id: str) -> list[Account]:
        if self._repository.get_customer(customer_id) is None:
            raise CustomerNotFoundError(f"No customer found with ID '{customer_id}'.")
        return self._repository.list_accounts_for_customer(customer_id)

    def _get_account_or_raise(self, account_id: str) -> Account:
        account = self._repository.get_account(account_id)
        if account is None:
            raise AccountNotFoundError(f"No account found with ID '{account_id}'.")
        return account

    def _record_transaction(self, account_id: str, txn_type: str, amount: Decimal, note: str) -> None:
        transaction = BankTransaction(
            id=uuid.uuid4().hex[:8], account_id=account_id, type=txn_type, amount=amount,
            timestamp=datetime.now().isoformat(timespec="seconds"), note=note,
        )
        self._repository.add_transaction(transaction)

    @staticmethod
    def _parse_amount(raw: str, allow_zero: bool = False) -> Decimal:
        try:
            amount = Decimal(raw)
        except InvalidOperation as exc:
            raise InvalidBankingDataError(f"Invalid amount: '{raw}'.") from exc
        if amount < 0 or (amount == 0 and not allow_zero):
            raise InvalidBankingDataError("Amount must be greater than zero.")
        return amount


def _print_menu() -> None:
    print("\n================================")
    print("   BANKING SYSTEM (EDUCATIONAL)")
    print("================================")
    print("1. Register customer")
    print("2. Open account")
    print("3. Deposit")
    print("4. Withdraw")
    print("5. Transfer")
    print("6. Balance inquiry")
    print("7. Transaction history")
    print("8. List customer accounts")
    print("0. Exit")


def _handle_register(service: BankingService) -> None:
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    try:
        customer = service.register_customer(name, email)
        print(f"Registered customer {customer.id}.")
    except BankingError as exc:
        print(f"Error: {exc}")


def _handle_open_account(service: BankingService) -> None:
    customer_id = input("Customer ID: ").strip()
    account_type = input("Account type (checking/savings): ").strip()
    opening_balance = input("Opening balance [0]: ").strip() or "0"
    try:
        account = service.open_account(customer_id, account_type, opening_balance)
        print(f"Opened account {account.id} with balance {account.balance}.")
    except BankingError as exc:
        print(f"Error: {exc}")


def _handle_deposit(service: BankingService) -> None:
    account_id = input("Account ID: ").strip()
    amount = input("Amount: ").strip()
    try:
        account = service.deposit(account_id, amount)
        print(f"New balance: {account.balance}")
    except BankingError as exc:
        print(f"Error: {exc}")


def _handle_withdraw(service: BankingService) -> None:
    account_id = input("Account ID: ").strip()
    amount = input("Amount: ").strip()
    try:
        account = service.withdraw(account_id, amount)
        print(f"New balance: {account.balance}")
    except BankingError as exc:
        print(f"Error: {exc}")


def _handle_transfer(service: BankingService) -> None:
    source = input("Source account ID: ").strip()
    target = input("Target account ID: ").strip()
    amount = input("Amount: ").strip()
    try:
        service.transfer(source, target, amount)
        print("Transfer completed.")
    except BankingError as exc:
        print(f"Error: {exc}")


def _handle_balance(service: BankingService) -> None:
    account_id = input("Account ID: ").strip()
    try:
        print(f"Balance: {service.balance_inquiry(account_id)}")
    except BankingError as exc:
        print(f"Error: {exc}")


def _handle_history(service: BankingService) -> None:
    account_id = input("Account ID: ").strip()
    try:
        transactions = service.transaction_history(account_id)
    except BankingError as exc:
        print(f"Error: {exc}")
        return
    if not transactions:
        print("No transactions found.")
        return
    for txn in transactions:
        print(f"[{txn.timestamp}] {txn.type}: {txn.amount} ({txn.note})")


def _handle_customer_accounts(service: BankingService) -> None:
    customer_id = input("Customer ID: ").strip()
    try:
        accounts = service.customer_accounts(customer_id)
    except BankingError as exc:
        print(f"Error: {exc}")
        return
    if not accounts:
        print("This customer has no accounts.")
        return
    for account in accounts:
        print(f"[{account.id}] {account.account_type} | balance={account.balance}")


def main() -> None:
    """Entry point for the interactive banking system CLI."""
    service = BankingService(BankRepository())
    actions = {
        "1": _handle_register,
        "2": _handle_open_account,
        "3": _handle_deposit,
        "4": _handle_withdraw,
        "5": _handle_transfer,
        "6": _handle_balance,
        "7": _handle_history,
        "8": _handle_customer_accounts,
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
