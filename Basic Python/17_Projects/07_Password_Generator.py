"""A secure, configurable password-generation utility.

Uses the `secrets` module (not `random`) for cryptographically secure
randomness, as required for any security-sensitive generation task.
"""

from __future__ import annotations

import logging
import string
from dataclasses import dataclass
from secrets import choice, SystemRandom

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

_SYSTEM_RANDOM = SystemRandom()


class PasswordGeneratorError(Exception):
    """Base exception for password-generation failures."""


class InvalidConfigurationError(PasswordGeneratorError):
    """Raised when the requested character-set configuration is invalid."""


@dataclass(slots=True, frozen=True)
class PasswordPolicy:
    """Configuration describing how a password should be generated."""

    length: int = 16
    use_uppercase: bool = True
    use_lowercase: bool = True
    use_digits: bool = True
    use_symbols: bool = True
    exclude_ambiguous: bool = False

    AMBIGUOUS_CHARS = "Il1O0"

    def character_pool(self) -> str:
        pool = ""
        if self.use_lowercase:
            pool += string.ascii_lowercase
        if self.use_uppercase:
            pool += string.ascii_uppercase
        if self.use_digits:
            pool += string.digits
        if self.use_symbols:
            pool += "!@#$%^&*()-_=+[]{};:,.?"
        if self.exclude_ambiguous:
            pool = "".join(c for c in pool if c not in self.AMBIGUOUS_CHARS)
        return pool

    def required_categories(self) -> list[str]:
        categories = []
        if self.use_lowercase:
            categories.append(string.ascii_lowercase)
        if self.use_uppercase:
            categories.append(string.ascii_uppercase)
        if self.use_digits:
            categories.append(string.digits)
        if self.use_symbols:
            categories.append("!@#$%^&*()-_=+[]{};:,.?")
        return categories


class PasswordStrength:
    """Evaluates the approximate strength of a generated password."""

    @staticmethod
    def evaluate(password: str) -> str:
        score = 0
        if len(password) >= 12:
            score += 1
        if len(password) >= 16:
            score += 1
        if any(c.islower() for c in password):
            score += 1
        if any(c.isupper() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(not c.isalnum() for c in password):
            score += 1

        if score <= 2:
            return "Weak"
        if score <= 4:
            return "Moderate"
        return "Strong"


class PasswordGeneratorService:
    """Generates secure passwords according to a given policy."""

    def generate(self, policy: PasswordPolicy) -> str:
        """Generate a single password matching the given policy.

        Raises:
            InvalidConfigurationError: If the policy is impossible to satisfy.
        """
        if policy.length < 4:
            raise InvalidConfigurationError("Password length must be at least 4.")

        pool = policy.character_pool()
        if not pool:
            raise InvalidConfigurationError("At least one character category must be enabled.")

        required_categories = policy.required_categories()
        if policy.length < len(required_categories):
            raise InvalidConfigurationError(
                "Password length must be at least as large as the number of "
                "enabled character categories."
            )

        # Guarantee at least one character from each enabled category.
        mandatory_chars = [choice(category) for category in required_categories]
        remaining_length = policy.length - len(mandatory_chars)
        remaining_chars = [choice(pool) for _ in range(remaining_length)]

        all_chars = mandatory_chars + remaining_chars
        _SYSTEM_RANDOM.shuffle(all_chars)
        return "".join(all_chars)

    def generate_batch(self, policy: PasswordPolicy, count: int) -> list[str]:
        if count < 1:
            raise InvalidConfigurationError("Count must be at least 1.")
        return [self.generate(policy) for _ in range(count)]


def _read_int(prompt: str, default: int) -> int:
    raw = input(f"{prompt} [{default}]: ").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        print("Invalid number, using default.")
        return default


def _read_bool(prompt: str, default: bool) -> bool:
    default_label = "Y/n" if default else "y/N"
    raw = input(f"{prompt} ({default_label}): ").strip().lower()
    if not raw:
        return default
    return raw in ("y", "yes")


def main() -> None:
    """Entry point for the interactive password generator CLI."""
    print("=== Secure Password Generator ===")
    service = PasswordGeneratorService()

    length = _read_int("Password length", 16)
    use_upper = _read_bool("Include uppercase letters?", True)
    use_lower = _read_bool("Include lowercase letters?", True)
    use_digits = _read_bool("Include digits?", True)
    use_symbols = _read_bool("Include symbols?", True)
    exclude_ambiguous = _read_bool("Exclude ambiguous characters (I, l, 1, O, 0)?", False)
    count = _read_int("How many passwords to generate?", 1)

    policy = PasswordPolicy(
        length=length,
        use_uppercase=use_upper,
        use_lowercase=use_lower,
        use_digits=use_digits,
        use_symbols=use_symbols,
        exclude_ambiguous=exclude_ambiguous,
    )

    try:
        passwords = service.generate_batch(policy, count)
    except PasswordGeneratorError as exc:
        print(f"Error: {exc}")
        return

    print("\nGenerated password(s):")
    for pwd in passwords:
        strength = PasswordStrength.evaluate(pwd)
        print(f"  {pwd}   (strength: {strength})")


if __name__ == "__main__":
    main()
