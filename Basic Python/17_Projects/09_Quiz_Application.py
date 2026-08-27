"""A reusable, configurable quiz application.

Separates question data, the quiz engine, scoring, and the CLI so the
engine can be tested independently of user interaction.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum


class QuizError(Exception):
    """Base exception for quiz-related failures."""


class NoActiveQuestionError(QuizError):
    """Raised when an answer is submitted with no active question."""


class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


@dataclass(slots=True, frozen=True)
class Question:
    """A single multiple-choice question."""

    prompt: str
    options: tuple[str, ...]
    correct_index: int
    category: str = "General"
    difficulty: Difficulty = Difficulty.MEDIUM

    def is_correct(self, chosen_index: int) -> bool:
        return chosen_index == self.correct_index


@dataclass(slots=True)
class QuizResult:
    """Outcome of a completed quiz session."""

    total_questions: int
    correct_answers: int

    @property
    def score_percentage(self) -> float:
        if self.total_questions == 0:
            return 0.0
        return round((self.correct_answers / self.total_questions) * 100, 1)


class QuestionBank:
    """Holds and filters the available pool of questions."""

    def __init__(self, questions: list[Question]) -> None:
        self._questions = questions

    def filter(
        self, category: str | None = None, difficulty: Difficulty | None = None
    ) -> list[Question]:
        results = self._questions
        if category is not None:
            results = [q for q in results if q.category == category]
        if difficulty is not None:
            results = [q for q in results if q.difficulty == difficulty]
        return list(results)

    @staticmethod
    def default_bank() -> QuestionBank:
        return QuestionBank([
            Question("What is the capital of France?",
                     ("Berlin", "Madrid", "Paris", "Rome"), 2, "Geography", Difficulty.EASY),
            Question("Which planet is known as the Red Planet?",
                     ("Venus", "Mars", "Jupiter", "Saturn"), 1, "Science", Difficulty.EASY),
            Question("What is the time complexity of binary search?",
                     ("O(n)", "O(log n)", "O(n^2)", "O(1)"), 1, "Computer Science", Difficulty.MEDIUM),
            Question("Who wrote 'Romeo and Juliet'?",
                     ("Charles Dickens", "Mark Twain", "William Shakespeare", "Jane Austen"),
                     2, "Literature", Difficulty.EASY),
            Question("What does 'CPU' stand for?",
                     ("Central Processing Unit", "Computer Personal Unit",
                      "Central Program Utility", "Core Processing Unit"),
                     0, "Computer Science", Difficulty.MEDIUM),
            Question("What is the chemical symbol for gold?",
                     ("Ag", "Au", "Gd", "Go"), 1, "Science", Difficulty.MEDIUM),
            Question("In which year did World War II end?",
                     ("1943", "1945", "1947", "1950"), 1, "History", Difficulty.MEDIUM),
            Question("What data structure uses FIFO ordering?",
                     ("Stack", "Queue", "Tree", "Graph"), 1, "Computer Science", Difficulty.HARD),
        ])


class QuizEngine:
    """Core quiz logic, decoupled from any user interface."""

    def __init__(self, question_bank: QuestionBank, rng: random.Random | None = None) -> None:
        self._question_bank = question_bank
        self._rng = rng or random.Random()
        self._questions: list[Question] = []
        self._current_index = -1
        self._correct_answers = 0

    def start_quiz(
        self,
        num_questions: int,
        category: str | None = None,
        difficulty: Difficulty | None = None,
    ) -> None:
        pool = self._question_bank.filter(category, difficulty)
        if not pool:
            raise QuizError("No questions match the given filters.")
        num_questions = min(num_questions, len(pool))
        self._questions = self._rng.sample(pool, num_questions)
        self._current_index = 0
        self._correct_answers = 0

    def current_question(self) -> Question | None:
        if 0 <= self._current_index < len(self._questions):
            return self._questions[self._current_index]
        return None

    def submit_answer(self, chosen_index: int) -> bool:
        question = self.current_question()
        if question is None:
            raise NoActiveQuestionError("No active question to answer.")
        correct = question.is_correct(chosen_index)
        if correct:
            self._correct_answers += 1
        self._current_index += 1
        return correct

    @property
    def is_finished(self) -> bool:
        return self._current_index >= len(self._questions)

    @property
    def total_questions(self) -> int:
        return len(self._questions)

    def result(self) -> QuizResult:
        return QuizResult(total_questions=len(self._questions), correct_answers=self._correct_answers)


def _print_question(question: Question, index: int, total: int) -> None:
    print(f"\nQuestion {index + 1}/{total} [{question.category} - {question.difficulty.value}]")
    print(question.prompt)
    for i, option in enumerate(question.options):
        print(f"  {i + 1}. {option}")


def _read_answer(num_options: int) -> int:
    while True:
        raw = input(f"Your answer (1-{num_options}): ").strip()
        try:
            choice = int(raw)
            if 1 <= choice <= num_options:
                return choice - 1
        except ValueError:
            pass
        print("Invalid choice, please try again.")


def _play_quiz(engine: QuizEngine) -> None:
    try:
        count_raw = input("How many questions? [5]: ").strip() or "5"
        count = int(count_raw)
        engine.start_quiz(count)
    except (ValueError, QuizError) as exc:
        print(f"Error: {exc}")
        return

    total = engine.total_questions
    index = 0
    while not engine.is_finished:
        question = engine.current_question()
        assert question is not None
        _print_question(question, index, total)
        chosen = _read_answer(len(question.options))
        correct = engine.submit_answer(chosen)
        print("Correct!" if correct else f"Incorrect. The right answer was: {question.options[question.correct_index]}")
        index += 1

    result = engine.result()
    print(f"\nQuiz complete! Score: {result.correct_answers}/{result.total_questions} "
          f"({result.score_percentage}%)")


def main() -> None:
    """Entry point for the interactive quiz CLI."""
    print("=== Quiz Application ===")
    engine = QuizEngine(QuestionBank.default_bank())

    while True:
        _play_quiz(engine)
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing. Goodbye.")
            break


if __name__ == "__main__":
    main()
