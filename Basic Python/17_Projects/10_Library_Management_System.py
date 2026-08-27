"""A professional library-management system backed by SQLite.

Architecture: Models -> LibraryRepository (SQLite persistence) ->
LibraryService (business rules) -> CLI (presentation).
"""

from __future__ import annotations

import logging
import sqlite3
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Iterator

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

DEFAULT_DB_PATH = Path.cwd() / "data" / "library.db"
LOAN_PERIOD_DAYS = 14


class LibraryError(Exception):
    """Base exception for library-related failures."""


class BookNotFoundError(LibraryError):
    """Raised when a requested book does not exist."""


class MemberNotFoundError(LibraryError):
    """Raised when a requested member does not exist."""


class BookUnavailableError(LibraryError):
    """Raised when attempting to borrow a book with no available copies."""


class LoanNotFoundError(LibraryError):
    """Raised when a return is attempted for a loan that does not exist."""


class InvalidLibraryDataError(LibraryError):
    """Raised when input data fails validation."""


@dataclass(slots=True)
class Book:
    id: str
    title: str
    author: str
    isbn: str
    total_copies: int
    available_copies: int


@dataclass(slots=True)
class Member:
    id: str
    name: str
    email: str


@dataclass(slots=True)
class Loan:
    id: str
    book_id: str
    member_id: str
    borrowed_on: str
    due_on: str
    returned_on: str | None


class LibraryRepository:
    """Handles SQLite persistence and schema management for the library."""

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
                CREATE TABLE IF NOT EXISTS books (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    isbn TEXT NOT NULL UNIQUE,
                    total_copies INTEGER NOT NULL,
                    available_copies INTEGER NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS members (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS loans (
                    id TEXT PRIMARY KEY,
                    book_id TEXT NOT NULL REFERENCES books(id),
                    member_id TEXT NOT NULL REFERENCES members(id),
                    borrowed_on TEXT NOT NULL,
                    due_on TEXT NOT NULL,
                    returned_on TEXT
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_loans_book ON loans(book_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_loans_member ON loans(member_id)")

    # --- Book persistence -------------------------------------------------
    def add_book(self, book: Book) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO books (id, title, author, isbn, total_copies, available_copies) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (book.id, book.title, book.author, book.isbn, book.total_copies, book.available_copies),
            )

    def get_book(self, book_id: str) -> Book | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
            return self._row_to_book(row) if row else None

    def update_book_availability(self, book_id: str, available_copies: int) -> None:
        with self._connect() as conn:
            conn.execute(
                "UPDATE books SET available_copies = ? WHERE id = ?", (available_copies, book_id)
            )

    def list_books(self) -> list[Book]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM books ORDER BY title").fetchall()
            return [self._row_to_book(r) for r in rows]

    def search_books(self, query: str) -> list[Book]:
        with self._connect() as conn:
            like = f"%{query}%"
            rows = conn.execute(
                "SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ? ORDER BY title",
                (like, like, like),
            ).fetchall()
            return [self._row_to_book(r) for r in rows]

    # --- Member persistence ------------------------------------------------
    def add_member(self, member: Member) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO members (id, name, email) VALUES (?, ?, ?)",
                (member.id, member.name, member.email),
            )

    def get_member(self, member_id: str) -> Member | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM members WHERE id = ?", (member_id,)).fetchone()
            return Member(row["id"], row["name"], row["email"]) if row else None

    def list_members(self) -> list[Member]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM members ORDER BY name").fetchall()
            return [Member(r["id"], r["name"], r["email"]) for r in rows]

    # --- Loan persistence ---------------------------------------------------
    def add_loan(self, loan: Loan) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO loans (id, book_id, member_id, borrowed_on, due_on, returned_on) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (loan.id, loan.book_id, loan.member_id, loan.borrowed_on, loan.due_on, loan.returned_on),
            )

    def get_loan(self, loan_id: str) -> Loan | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM loans WHERE id = ?", (loan_id,)).fetchone()
            return self._row_to_loan(row) if row else None

    def mark_loan_returned(self, loan_id: str, returned_on: str) -> None:
        with self._connect() as conn:
            conn.execute("UPDATE loans SET returned_on = ? WHERE id = ?", (returned_on, loan_id))

    def list_active_loans(self) -> list[Loan]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM loans WHERE returned_on IS NULL").fetchall()
            return [self._row_to_loan(r) for r in rows]

    def list_loans_for_member(self, member_id: str) -> list[Loan]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM loans WHERE member_id = ? ORDER BY borrowed_on DESC", (member_id,)
            ).fetchall()
            return [self._row_to_loan(r) for r in rows]

    @staticmethod
    def _row_to_book(row: sqlite3.Row) -> Book:
        return Book(row["id"], row["title"], row["author"], row["isbn"],
                    row["total_copies"], row["available_copies"])

    @staticmethod
    def _row_to_loan(row: sqlite3.Row) -> Loan:
        return Loan(row["id"], row["book_id"], row["member_id"],
                    row["borrowed_on"], row["due_on"], row["returned_on"])


class LibraryService:
    """Business rules for the library, independent of persistence details."""

    def __init__(self, repository: LibraryRepository) -> None:
        self._repository = repository

    def add_book(self, title: str, author: str, isbn: str, copies: int) -> Book:
        title, author, isbn = title.strip(), author.strip(), isbn.strip()
        if not title or not author or not isbn:
            raise InvalidLibraryDataError("Title, author, and ISBN are required.")
        if copies < 1:
            raise InvalidLibraryDataError("Copies must be at least 1.")

        book = Book(id=uuid.uuid4().hex[:8], title=title, author=author,
                    isbn=isbn, total_copies=copies, available_copies=copies)
        try:
            self._repository.add_book(book)
        except sqlite3.IntegrityError as exc:
            raise InvalidLibraryDataError(f"A book with ISBN '{isbn}' already exists.") from exc
        return book

    def register_member(self, name: str, email: str) -> Member:
        name, email = name.strip(), email.strip().lower()
        if not name or not email:
            raise InvalidLibraryDataError("Name and email are required.")
        member = Member(id=uuid.uuid4().hex[:8], name=name, email=email)
        try:
            self._repository.add_member(member)
        except sqlite3.IntegrityError as exc:
            raise InvalidLibraryDataError(f"A member with email '{email}' already exists.") from exc
        return member

    def borrow_book(self, book_id: str, member_id: str) -> Loan:
        book = self._repository.get_book(book_id)
        if book is None:
            raise BookNotFoundError(f"No book found with ID '{book_id}'.")
        if self._repository.get_member(member_id) is None:
            raise MemberNotFoundError(f"No member found with ID '{member_id}'.")
        if book.available_copies < 1:
            raise BookUnavailableError(f"'{book.title}' has no available copies.")

        today = date.today()
        loan = Loan(
            id=uuid.uuid4().hex[:8], book_id=book_id, member_id=member_id,
            borrowed_on=today.isoformat(),
            due_on=(today + timedelta(days=LOAN_PERIOD_DAYS)).isoformat(),
            returned_on=None,
        )
        self._repository.add_loan(loan)
        self._repository.update_book_availability(book_id, book.available_copies - 1)
        return loan

    def return_book(self, loan_id: str) -> Loan:
        loan = self._repository.get_loan(loan_id)
        if loan is None:
            raise LoanNotFoundError(f"No loan found with ID '{loan_id}'.")
        if loan.returned_on is not None:
            raise LibraryError("This book has already been returned.")

        book = self._repository.get_book(loan.book_id)
        if book is None:
            raise BookNotFoundError(f"No book found with ID '{loan.book_id}'.")

        returned_on = date.today().isoformat()
        self._repository.mark_loan_returned(loan_id, returned_on)
        self._repository.update_book_availability(
            loan.book_id, min(book.total_copies, book.available_copies + 1)
        )
        loan.returned_on = returned_on
        return loan

    def overdue_loans(self) -> list[Loan]:
        today = date.today().isoformat()
        return [loan for loan in self._repository.list_active_loans() if loan.due_on < today]

    def search_books(self, query: str) -> list[Book]:
        return self._repository.search_books(query)

    def list_books(self) -> list[Book]:
        return self._repository.list_books()

    def list_members(self) -> list[Member]:
        return self._repository.list_members()

    def member_history(self, member_id: str) -> list[Loan]:
        if self._repository.get_member(member_id) is None:
            raise MemberNotFoundError(f"No member found with ID '{member_id}'.")
        return self._repository.list_loans_for_member(member_id)


def _print_menu() -> None:
    print("\n================================")
    print("   LIBRARY MANAGEMENT SYSTEM")
    print("================================")
    print("1. Add book")
    print("2. Register member")
    print("3. List books")
    print("4. Search books")
    print("5. Borrow book")
    print("6. Return book")
    print("7. Overdue loans")
    print("8. Member loan history")
    print("0. Exit")


def _read_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Please enter a whole number.")


def _handle_add_book(service: LibraryService) -> None:
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    isbn = input("ISBN: ").strip()
    copies = _read_int("Number of copies: ")
    try:
        book = service.add_book(title, author, isbn, copies)
        print(f"Added book {book.id}.")
    except LibraryError as exc:
        print(f"Error: {exc}")


def _handle_register_member(service: LibraryService) -> None:
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    try:
        member = service.register_member(name, email)
        print(f"Registered member {member.id}.")
    except LibraryError as exc:
        print(f"Error: {exc}")


def _handle_list_books(service: LibraryService) -> None:
    books = service.list_books()
    if not books:
        print("No books found.")
        return
    for book in books:
        print(f"[{book.id}] {book.title} by {book.author} | "
              f"available {book.available_copies}/{book.total_copies}")


def _handle_search_books(service: LibraryService) -> None:
    query = input("Search query: ").strip()
    results = service.search_books(query)
    if not results:
        print("No matching books.")
        return
    for book in results:
        print(f"[{book.id}] {book.title} by {book.author} | "
              f"available {book.available_copies}/{book.total_copies}")


def _handle_borrow(service: LibraryService) -> None:
    book_id = input("Book ID: ").strip()
    member_id = input("Member ID: ").strip()
    try:
        loan = service.borrow_book(book_id, member_id)
        print(f"Loan created: {loan.id} (due {loan.due_on}).")
    except LibraryError as exc:
        print(f"Error: {exc}")


def _handle_return(service: LibraryService) -> None:
    loan_id = input("Loan ID: ").strip()
    try:
        loan = service.return_book(loan_id)
        print(f"Book returned on {loan.returned_on}.")
    except LibraryError as exc:
        print(f"Error: {exc}")


def _handle_overdue(service: LibraryService) -> None:
    loans = service.overdue_loans()
    if not loans:
        print("No overdue loans.")
        return
    for loan in loans:
        print(f"[{loan.id}] book={loan.book_id} member={loan.member_id} due={loan.due_on}")


def _handle_member_history(service: LibraryService) -> None:
    member_id = input("Member ID: ").strip()
    try:
        loans = service.member_history(member_id)
    except LibraryError as exc:
        print(f"Error: {exc}")
        return
    if not loans:
        print("No loan history.")
        return
    for loan in loans:
        status = f"returned {loan.returned_on}" if loan.returned_on else f"due {loan.due_on}"
        print(f"[{loan.id}] book={loan.book_id} | {status}")


def main() -> None:
    """Entry point for the interactive library management CLI."""
    service = LibraryService(LibraryRepository())
    actions = {
        "1": _handle_add_book,
        "2": _handle_register_member,
        "3": _handle_list_books,
        "4": _handle_search_books,
        "5": _handle_borrow,
        "6": _handle_return,
        "7": _handle_overdue,
        "8": _handle_member_history,
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
