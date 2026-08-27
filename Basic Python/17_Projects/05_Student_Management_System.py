"""A professional student-management application.

Architecture: Models -> Repository (JSON persistence) -> Service
(business rules & reporting) -> CLI (presentation).
"""

from __future__ import annotations

import json
import logging
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

DEFAULT_STORAGE_PATH = Path.cwd() / "data" / "students.json"
GRADE_POINTS = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}


class StudentError(Exception):
    """Base exception for student-related failures."""


class StudentNotFoundError(StudentError):
    """Raised when a requested student ID does not exist."""


class InvalidStudentDataError(StudentError):
    """Raised when student input data fails validation."""


@dataclass(slots=True)
class Subject:
    """A subject enrollment with an associated letter grade."""

    name: str
    grade: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> Subject:
        return cls(**data)


@dataclass(slots=True)
class Student:
    """Represents a single student record."""

    name: str
    email: str
    department: str
    semester: int
    subjects: list[Subject] = field(default_factory=list)
    student_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])

    def to_dict(self) -> dict:
        data = asdict(self)
        data["subjects"] = [s.to_dict() for s in self.subjects]
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Student:
        subjects = [Subject.from_dict(s) for s in data.get("subjects", [])]
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            email=data["email"],
            department=data["department"],
            semester=data["semester"],
            subjects=subjects,
        )


class StudentRepository:
    """Handles JSON persistence for student records."""

    def __init__(self, storage_path: Path = DEFAULT_STORAGE_PATH) -> None:
        self._storage_path = storage_path
        self._storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not self._storage_path.exists():
            self._write_all([])

    def load_all(self) -> list[Student]:
        try:
            raw = self._storage_path.read_text(encoding="utf-8")
            payload = json.loads(raw) if raw.strip() else []
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Failed to load students (%s); starting with empty list.", exc)
            return []
        return [Student.from_dict(item) for item in payload]

    def save_all(self, students: list[Student]) -> None:
        self._write_all([s.to_dict() for s in students])

    def _write_all(self, payload: list[dict]) -> None:
        tmp_path = self._storage_path.with_suffix(".tmp")
        tmp_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        tmp_path.replace(self._storage_path)


class StudentService:
    """Business logic for managing students, independent of any UI."""

    def __init__(self, repository: StudentRepository) -> None:
        self._repository = repository
        self._students: dict[str, Student] = {s.student_id: s for s in repository.load_all()}

    def register_student(self, name: str, email: str, department: str, semester: int) -> Student:
        name, email, department = name.strip(), email.strip().lower(), department.strip()
        if not name or not email or not department:
            raise InvalidStudentDataError("Name, email, and department are required.")
        if semester < 1:
            raise InvalidStudentDataError("Semester must be a positive integer.")

        student = Student(name=name, email=email, department=department, semester=semester)
        self._students[student.student_id] = student
        self._persist()
        return student

    def add_subject_grade(self, student_id: str, subject_name: str, grade: str) -> Student:
        student = self._get_or_raise(student_id)
        grade = grade.strip().upper()
        if grade not in GRADE_POINTS:
            raise InvalidStudentDataError(f"Invalid grade '{grade}'. Use A, B, C, D, or F.")
        subject_name = subject_name.strip()
        if not subject_name:
            raise InvalidStudentDataError("Subject name cannot be empty.")

        existing = next((s for s in student.subjects if s.name == subject_name), None)
        if existing:
            existing.grade = grade
        else:
            student.subjects.append(Subject(name=subject_name, grade=grade))
        self._persist()
        return student

    def calculate_gpa(self, student_id: str) -> float:
        student = self._get_or_raise(student_id)
        if not student.subjects:
            return 0.0
        total_points = sum(GRADE_POINTS[s.grade] for s in student.subjects)
        return round(total_points / len(student.subjects), 2)

    def update_student(self, student_id: str, **fields) -> Student:
        student = self._get_or_raise(student_id)
        if fields.get("name"):
            student.name = fields["name"].strip()
        if fields.get("email"):
            student.email = fields["email"].strip().lower()
        if fields.get("department"):
            student.department = fields["department"].strip()
        if fields.get("semester") is not None:
            if fields["semester"] < 1:
                raise InvalidStudentDataError("Semester must be a positive integer.")
            student.semester = fields["semester"]
        self._persist()
        return student

    def delete_student(self, student_id: str) -> None:
        self._get_or_raise(student_id)
        del self._students[student_id]
        self._persist()

    def search(self, query: str) -> list[Student]:
        query = query.strip().lower()
        if not query:
            return self.list_students()
        return [
            s for s in self._students.values()
            if query in s.name.lower() or query in s.email.lower() or query in s.department.lower()
        ]

    def list_students(self) -> list[Student]:
        return sorted(self._students.values(), key=lambda s: s.name.lower())

    def performance_report(self, student_id: str) -> str:
        student = self._get_or_raise(student_id)
        lines = [f"Performance report for {student.name} ({student.student_id})"]
        for subject in student.subjects:
            lines.append(f"  {subject.name}: {subject.grade}")
        lines.append(f"  GPA: {self.calculate_gpa(student_id)}")
        return "\n".join(lines)

    def _get_or_raise(self, student_id: str) -> Student:
        student = self._students.get(student_id)
        if student is None:
            raise StudentNotFoundError(f"No student found with ID '{student_id}'.")
        return student

    def _persist(self) -> None:
        self._repository.save_all(list(self._students.values()))


def _print_menu() -> None:
    print("\n================================")
    print("   STUDENT MANAGEMENT SYSTEM")
    print("================================")
    print("1. Register student")
    print("2. List students")
    print("3. Search students")
    print("4. Add/update subject grade")
    print("5. Update student profile")
    print("6. Delete student")
    print("7. Performance report")
    print("0. Exit")


def _print_student(student: Student) -> None:
    print(f"[{student.student_id}] {student.name} | {student.department} "
          f"| semester {student.semester} | {student.email}")


def _read_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Please enter a whole number.")


def _handle_register(service: StudentService) -> None:
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    department = input("Department: ").strip()
    semester = _read_int("Semester: ")
    try:
        student = service.register_student(name, email, department, semester)
        print(f"Registered student {student.student_id}.")
    except StudentError as exc:
        print(f"Error: {exc}")


def _handle_list(service: StudentService) -> None:
    students = service.list_students()
    if not students:
        print("No students found.")
        return
    for student in students:
        _print_student(student)


def _handle_search(service: StudentService) -> None:
    query = input("Search query: ").strip()
    results = service.search(query)
    if not results:
        print("No matching students.")
        return
    for student in results:
        _print_student(student)


def _handle_add_grade(service: StudentService) -> None:
    student_id = input("Student ID: ").strip()
    subject = input("Subject name: ").strip()
    grade = input("Grade (A/B/C/D/F): ").strip()
    try:
        service.add_subject_grade(student_id, subject, grade)
        print("Grade recorded.")
    except StudentError as exc:
        print(f"Error: {exc}")


def _handle_update(service: StudentService) -> None:
    student_id = input("Student ID: ").strip()
    name = input("New name (leave blank to keep): ").strip() or None
    department = input("New department (leave blank to keep): ").strip() or None
    try:
        service.update_student(student_id, name=name, department=department)
        print("Student updated.")
    except StudentError as exc:
        print(f"Error: {exc}")


def _handle_delete(service: StudentService) -> None:
    student_id = input("Student ID: ").strip()
    try:
        service.delete_student(student_id)
        print("Student deleted.")
    except StudentError as exc:
        print(f"Error: {exc}")


def _handle_report(service: StudentService) -> None:
    student_id = input("Student ID: ").strip()
    try:
        print(service.performance_report(student_id))
    except StudentError as exc:
        print(f"Error: {exc}")


def main() -> None:
    """Entry point for the interactive student management CLI."""
    service = StudentService(StudentRepository())
    actions = {
        "1": _handle_register,
        "2": _handle_list,
        "3": _handle_search,
        "4": _handle_add_grade,
        "5": _handle_update,
        "6": _handle_delete,
        "7": _handle_report,
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
