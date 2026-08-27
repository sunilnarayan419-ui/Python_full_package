"""A reusable text-analysis application.

Pipeline: text input -> processing -> analysis -> reporting, using
only standard-library tools (re, collections.Counter, pathlib).
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

DEFAULT_STOP_WORDS: frozenset[str] = frozenset({
    "the", "a", "an", "and", "or", "but", "is", "are", "was", "were", "in",
    "on", "at", "to", "for", "of", "with", "by", "this", "that", "it", "as",
    "be", "from", "has", "have", "had", "not", "so", "if",
})

WORD_PATTERN = re.compile(r"[A-Za-z']+")
SENTENCE_PATTERN = re.compile(r"[.!?]+(?:\s|$)")


class TextAnalyzerError(Exception):
    """Base exception for text-analysis failures."""


class EmptyTextError(TextAnalyzerError):
    """Raised when the input text is empty or whitespace-only."""


@dataclass(slots=True, frozen=True)
class AnalysisResult:
    """Structured result of a full text analysis."""

    character_count: int
    character_count_no_spaces: int
    word_count: int
    sentence_count: int
    line_count: int
    average_word_length: float
    word_frequencies: Counter[str]
    punctuation_counts: Counter[str]

    def most_common_words(self, n: int = 10) -> list[tuple[str, int]]:
        return self.word_frequencies.most_common(n)

    def report(self, top_n: int = 10) -> str:
        lines = [
            "=== Text Analysis Report ===",
            f"Characters (total):        {self.character_count}",
            f"Characters (no spaces):    {self.character_count_no_spaces}",
            f"Words:                     {self.word_count}",
            f"Sentences:                 {self.sentence_count}",
            f"Lines:                     {self.line_count}",
            f"Average word length:       {self.average_word_length:.2f}",
            "",
            f"Top {top_n} most common words:",
        ]
        for word, count in self.most_common_words(top_n):
            lines.append(f"  {word}: {count}")
        if self.punctuation_counts:
            lines.append("")
            lines.append("Punctuation usage:")
            for mark, count in self.punctuation_counts.most_common():
                lines.append(f"  '{mark}': {count}")
        return "\n".join(lines)


class TextAnalyzer:
    """Performs statistical analysis of a block of text."""

    def __init__(self, stop_words: frozenset[str] = DEFAULT_STOP_WORDS) -> None:
        self._stop_words = stop_words

    def analyze(self, text: str, exclude_stop_words: bool = False) -> AnalysisResult:
        """Analyze `text` and return a structured result.

        Raises:
            EmptyTextError: If the text is empty or whitespace-only.
        """
        if not text.strip():
            raise EmptyTextError("Cannot analyze empty text.")

        words = [w.lower() for w in WORD_PATTERN.findall(text)]
        analyzable_words = (
            [w for w in words if w not in self._stop_words] if exclude_stop_words else words
        )

        sentences = [s for s in SENTENCE_PATTERN.split(text) if s.strip()]
        lines = text.splitlines() or [text]
        punctuation = Counter(c for c in text if c in ".,!?;:'\"-()")

        total_word_length = sum(len(w) for w in words)
        avg_word_length = total_word_length / len(words) if words else 0.0

        return AnalysisResult(
            character_count=len(text),
            character_count_no_spaces=len(text.replace(" ", "").replace("\n", "").replace("\t", "")),
            word_count=len(words),
            sentence_count=len(sentences),
            line_count=len(lines),
            average_word_length=avg_word_length,
            word_frequencies=Counter(analyzable_words),
            punctuation_counts=punctuation,
        )

    @staticmethod
    def load_text_from_file(path: Path) -> str:
        if not path.exists():
            raise TextAnalyzerError(f"File not found: {path}")
        try:
            return path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            raise TextAnalyzerError(f"Failed to read file: {exc}") from exc


def _print_menu() -> None:
    print("\n================================")
    print("         TEXT ANALYZER")
    print("================================")
    print("1. Analyze typed text")
    print("2. Analyze text from a file")
    print("0. Exit")


def _handle_typed_text(analyzer: TextAnalyzer) -> None:
    print("Enter text (finish with an empty line):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    text = "\n".join(lines)

    exclude_stop = input("Exclude common stop words? (y/N): ").strip().lower() == "y"
    try:
        result = analyzer.analyze(text, exclude_stop_words=exclude_stop)
        print("\n" + result.report())
    except TextAnalyzerError as exc:
        print(f"Error: {exc}")


def _handle_file_text(analyzer: TextAnalyzer) -> None:
    raw_path = input("File path: ").strip()
    exclude_stop = input("Exclude common stop words? (y/N): ").strip().lower() == "y"
    try:
        text = TextAnalyzer.load_text_from_file(Path(raw_path).expanduser())
        result = analyzer.analyze(text, exclude_stop_words=exclude_stop)
        print("\n" + result.report())
    except TextAnalyzerError as exc:
        print(f"Error: {exc}")


def main() -> None:
    """Entry point for the interactive text analyzer CLI."""
    analyzer = TextAnalyzer()

    while True:
        _print_menu()
        choice = input("Select an option: ").strip()
        if choice == "0":
            print("Goodbye.")
            break
        elif choice == "1":
            _handle_typed_text(analyzer)
        elif choice == "2":
            _handle_file_text(analyzer)
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
