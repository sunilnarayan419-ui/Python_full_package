"""A professional command-line number-guessing game.

Separates game logic (testable, deterministic given a seeded RNG) from
the CLI presentation layer, and supports configurable difficulty levels.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum


class GameError(Exception):
    """Base exception for game-related failures."""


class GuessOutOfRangeError(GameError):
    """Raised when a guess falls outside the configured range."""


class Difficulty(Enum):
    EASY = "1"
    MEDIUM = "2"
    HARD = "3"

    @property
    def settings(self) -> tuple[int, int, int]:
        """Return (minimum, maximum, max_attempts) for this difficulty."""
        return {
            Difficulty.EASY: (1, 50, 10),
            Difficulty.MEDIUM: (1, 100, 7),
            Difficulty.HARD: (1, 200, 5),
        }[self]

    @property
    def label(self) -> str:
        return self.name.title()


@dataclass(slots=True)
class GameState:
    """Mutable state for a single round of the guessing game."""

    minimum: int
    maximum: int
    max_attempts: int
    target: int
    attempts_used: int = 0
    guesses: list[int] = field(default_factory=list)
    won: bool = False

    @property
    def attempts_remaining(self) -> int:
        return self.max_attempts - self.attempts_used

    @property
    def is_over(self) -> bool:
        return self.won or self.attempts_remaining <= 0


class NumberGuessingGame:
    """Core game engine, decoupled from any user interface."""

    def __init__(self, rng: random.Random | None = None) -> None:
        self._rng = rng or random.Random()
        self._state: GameState | None = None

    def start_new_game(self, difficulty: Difficulty) -> GameState:
        minimum, maximum, max_attempts = difficulty.settings
        target = self._rng.randint(minimum, maximum)
        self._state = GameState(minimum, maximum, max_attempts, target)
        return self._state

    def submit_guess(self, guess: int) -> str:
        """Process a guess and return 'higher', 'lower', or 'correct'.

        Raises:
            GameError: If no game is active or it has already ended.
            GuessOutOfRangeError: If the guess is outside the valid range.
        """
        state = self._require_active_state()
        if not (state.minimum <= guess <= state.maximum):
            raise GuessOutOfRangeError(
                f"Guess must be between {state.minimum} and {state.maximum}."
            )

        state.attempts_used += 1
        state.guesses.append(guess)

        if guess == state.target:
            state.won = True
            return "correct"
        return "higher" if guess < state.target else "lower"

    def calculate_score(self) -> int:
        """Compute a score based on attempts used and range size."""
        state = self._require_active_state()
        if not state.won:
            return 0
        range_size = state.maximum - state.minimum + 1
        efficiency_bonus = max(0, state.max_attempts - state.attempts_used) * 10
        return range_size // 10 + efficiency_bonus + 50

    def _require_active_state(self) -> GameState:
        if self._state is None:
            raise GameError("No game has been started.")
        return self._state


def _read_difficulty() -> Difficulty:
    print("\nSelect difficulty:")
    for difficulty in Difficulty:
        low, high, attempts = difficulty.settings
        print(f"{difficulty.value}. {difficulty.label} (range {low}-{high}, {attempts} attempts)")
    while True:
        choice = input("Your choice: ").strip()
        try:
            return Difficulty(choice)
        except ValueError:
            print("Invalid choice, please try again.")


def _read_guess(minimum: int, maximum: int) -> int:
    while True:
        raw = input(f"Enter your guess ({minimum}-{maximum}): ").strip()
        try:
            return int(raw)
        except ValueError:
            print("Please enter a whole number.")


def _play_round(game: NumberGuessingGame) -> None:
    difficulty = _read_difficulty()
    state = game.start_new_game(difficulty)
    print(f"\nI'm thinking of a number between {state.minimum} and {state.maximum}.")
    print(f"You have {state.max_attempts} attempts. Good luck!")

    while not state.is_over:
        guess = _read_guess(state.minimum, state.maximum)
        try:
            outcome = game.submit_guess(guess)
        except GuessOutOfRangeError as exc:
            print(f"Invalid guess: {exc}")
            continue

        if outcome == "correct":
            print(f"Correct! You guessed it in {state.attempts_used} attempts.")
            print(f"Score: {game.calculate_score()}")
        else:
            print(f"Too {'low' if outcome == 'higher' else 'high'}.")
            if state.attempts_remaining > 0:
                print(f"Attempts remaining: {state.attempts_remaining}")
            else:
                print(f"Out of attempts. The number was {state.target}.")


def main() -> None:
    """Entry point for the interactive guessing game CLI."""
    game = NumberGuessingGame()
    print("Welcome to Guess the Number.")

    while True:
        _play_round(game)
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing. Goodbye.")
            break


if __name__ == "__main__":
    main()
