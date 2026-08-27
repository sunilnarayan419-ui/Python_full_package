"""A persistent, professional contact-management application."""

from __future__ import annotations

import json
import logging
import re
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

DEFAULT_STORAGE_PATH = Path.cwd() / "data" / "contacts.json"
EMAIL_PATTERN = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")
PHONE_PATTERN = re.compile(r"^\+?[0-9()\-\s]{7,20}$")


class ContactError(Exception):
    """Base exception for contact-related failures."""


class ContactNotFoundError(ContactError):
    """Raised when a requested contact ID does not exist."""


class InvalidContactDataError(ContactError):
    """Raised when contact input data fails validation."""


class DuplicateContactError(ContactError):
    """Raised when a contact with the same email already exists."""


@dataclass(slots=True)
class Contact:
    """Represents a single contact entry."""

    name: str
    phone: str
    email: str
    organization: str = ""
    notes: str = ""
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> Contact:
        return cls(**data)


class ContactRepository:
    """Handles JSON persistence for contacts."""

    def __init__(self, storage_path: Path = DEFAULT_STORAGE_PATH) -> None:
        self._storage_path = storage_path
        self._storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not self._storage_path.exists():
            self._write_all([])

    def load_all(self) -> list[Contact]:
        try:
            raw = self._storage_path.read_text(encoding="utf-8")
            payload = json.loads(raw) if raw.strip() else []
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Failed to load contacts (%s); starting with empty list.", exc)
            return []
        return [Contact.from_dict(item) for item in payload]

    def save_all(self, contacts: list[Contact]) -> None:
        self._write_all([contact.to_dict() for contact in contacts])

    def _write_all(self, payload: list[dict]) -> None:
        tmp_path = self._storage_path.with_suffix(".tmp")
        tmp_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        tmp_path.replace(self._storage_path)


class ContactService:
    """Business logic for managing contacts, independent of any UI."""

    def __init__(self, repository: ContactRepository) -> None:
        self._repository = repository
        self._contacts: dict[str, Contact] = {c.id: c for c in repository.load_all()}

    def add_contact(
        self, name: str, phone: str, email: str, organization: str = "", notes: str = ""
    ) -> Contact:
        name, phone, email = name.strip(), phone.strip(), email.strip().lower()
        self._validate(name, phone, email)
        if any(c.email == email for c in self._contacts.values()):
            raise DuplicateContactError(f"A contact with email '{email}' already exists.")

        contact = Contact(name=name, phone=phone, email=email,
                           organization=organization.strip(), notes=notes.strip())
        self._contacts[contact.id] = contact
        self._persist()
        return contact

    def update_contact(self, contact_id: str, **fields) -> Contact:
        contact = self._get_or_raise(contact_id)
        if fields.get("name"):
            contact.name = fields["name"].strip()
        if fields.get("phone"):
            phone = fields["phone"].strip()
            if not PHONE_PATTERN.match(phone):
                raise InvalidContactDataError(f"Invalid phone number: '{phone}'.")
            contact.phone = phone
        if fields.get("email"):
            email = fields["email"].strip().lower()
            if not EMAIL_PATTERN.match(email):
                raise InvalidContactDataError(f"Invalid email address: '{email}'.")
            contact.email = email
        if fields.get("organization") is not None:
            contact.organization = fields["organization"].strip()
        if fields.get("notes") is not None:
            contact.notes = fields["notes"].strip()
        self._persist()
        return contact

    def delete_contact(self, contact_id: str) -> None:
        self._get_or_raise(contact_id)
        del self._contacts[contact_id]
        self._persist()

    def search(self, query: str) -> list[Contact]:
        query = query.strip().lower()
        if not query:
            return self.list_contacts()
        return [
            c for c in self._contacts.values()
            if query in c.name.lower() or query in c.email.lower()
            or query in c.phone or query in c.organization.lower()
        ]

    def list_contacts(self) -> list[Contact]:
        return sorted(self._contacts.values(), key=lambda c: c.name.lower())

    def _get_or_raise(self, contact_id: str) -> Contact:
        contact = self._contacts.get(contact_id)
        if contact is None:
            raise ContactNotFoundError(f"No contact found with ID '{contact_id}'.")
        return contact

    @staticmethod
    def _validate(name: str, phone: str, email: str) -> None:
        if not name:
            raise InvalidContactDataError("Contact name cannot be empty.")
        if not PHONE_PATTERN.match(phone):
            raise InvalidContactDataError(f"Invalid phone number: '{phone}'.")
        if not EMAIL_PATTERN.match(email):
            raise InvalidContactDataError(f"Invalid email address: '{email}'.")

    def _persist(self) -> None:
        self._repository.save_all(list(self._contacts.values()))


def _print_menu() -> None:
    print("\n================================")
    print("          CONTACT BOOK")
    print("================================")
    print("1. Add contact")
    print("2. List contacts")
    print("3. Search contacts")
    print("4. Update contact")
    print("5. Delete contact")
    print("0. Exit")


def _print_contact(contact: Contact) -> None:
    org = f" ({contact.organization})" if contact.organization else ""
    print(f"[{contact.id}] {contact.name}{org} | {contact.phone} | {contact.email}")


def _handle_add(service: ContactService) -> None:
    name = input("Name: ").strip()
    phone = input("Phone: ").strip()
    email = input("Email: ").strip()
    organization = input("Organization (optional): ").strip()
    notes = input("Notes (optional): ").strip()
    try:
        contact = service.add_contact(name, phone, email, organization, notes)
        print(f"Added contact {contact.id}.")
    except ContactError as exc:
        print(f"Error: {exc}")


def _handle_list(service: ContactService) -> None:
    contacts = service.list_contacts()
    if not contacts:
        print("No contacts found.")
        return
    for contact in contacts:
        _print_contact(contact)


def _handle_search(service: ContactService) -> None:
    query = input("Search query: ").strip()
    results = service.search(query)
    if not results:
        print("No matching contacts.")
        return
    for contact in results:
        _print_contact(contact)


def _handle_update(service: ContactService) -> None:
    contact_id = input("Contact ID: ").strip()
    name = input("New name (leave blank to keep): ").strip() or None
    phone = input("New phone (leave blank to keep): ").strip() or None
    email = input("New email (leave blank to keep): ").strip() or None
    try:
        contact = service.update_contact(contact_id, name=name, phone=phone, email=email)
        print(f"Updated contact {contact.id}.")
    except ContactError as exc:
        print(f"Error: {exc}")


def _handle_delete(service: ContactService) -> None:
    contact_id = input("Contact ID: ").strip()
    try:
        service.delete_contact(contact_id)
        print("Contact deleted.")
    except ContactError as exc:
        print(f"Error: {exc}")


def main() -> None:
    """Entry point for the interactive contact book CLI."""
    service = ContactService(ContactRepository())
    actions = {
        "1": _handle_add,
        "2": _handle_list,
        "3": _handle_search,
        "4": _handle_update,
        "5": _handle_delete,
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
