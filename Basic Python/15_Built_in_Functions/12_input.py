"""Demonstrations of the built-in input() function using laboratory data entry.

Actual input() usage is isolated in dedicated methods so the module remains
fully executable in automated, non-interactive environments.
"""


class UniversityInput:
    """Teach the fundamental behavior of input() for collecting user data."""

    def prompt_for_species(self) -> str:
        """Isolated method that performs real interactive input()."""
        return input("Enter plant species: ")

    @staticmethod
    def demo_species(species: str) -> str:
        """Deterministic demonstration path that does not call input()."""
        return f"Recorded species: {species}"

    @staticmethod
    def run() -> None:
        # Deterministic demonstration; interactive input() is available via
        # UniversityInput().prompt_for_species() but is not called here.
        simulated_species = "Wheat"
        print(UniversityInput.demo_species(simulated_species))


class InterviewInput:
    """Validate user-provided scientific data before accepting it."""

    def prompt_for_height(self) -> float:
        """Isolated interactive method: reads and validates a real input()."""
        raw_value = input("Enter plant height (cm): ")
        return self.validate_height(raw_value)

    @staticmethod
    def validate_height(raw_value: str) -> float:
        """Convert and validate a raw string into a plausible plant height."""
        try:
            height = float(raw_value)
        except ValueError as exc:
            raise ValueError(f"'{raw_value}' is not a valid number") from exc

        if height <= 0:
            raise ValueError(f"Height must be positive, got {height}")

        return height

    @staticmethod
    def run() -> None:
        test_cases = ["58.2", "not_a_number", "-5.0", "0"]

        for raw_value in test_cases:
            try:
                validated = InterviewInput.validate_height(raw_value)
                print(f"'{raw_value}' -> valid height: {validated} cm")
            except ValueError as error:
                print(f"'{raw_value}' -> invalid: {error}")


class IndustryInput:
    """Safe interactive scientific-data collection workflow."""

    def __init__(self) -> None:
        self.collected_samples: list[dict[str, object]] = []

    def collect_sample_interactively(self) -> dict[str, object]:
        """Real interactive collection path, isolated from automated demos."""
        sample_id = input("Sample ID: ")
        raw_height = input("Height (cm): ")
        height = InterviewInput.validate_height(raw_height)
        record = {"sample_id": sample_id, "height": height}
        self.collected_samples.append(record)
        return record

    def collect_sample_from_source(self, sample_id: str, raw_height: str) -> dict[str, object]:
        """Deterministic path used for automated demonstration and testing."""
        height = InterviewInput.validate_height(raw_height)
        record = {"sample_id": sample_id, "height": height}
        self.collected_samples.append(record)
        return record

    @staticmethod
    def run() -> None:
        collector = IndustryInput()
        simulated_entries = [("S001", "58.2"), ("S002", "61.4")]

        for sample_id, raw_height in simulated_entries:
            record = collector.collect_sample_from_source(sample_id, raw_height)
            print(f"Collected: {record}")

        print(f"Total samples collected: {len(collector.collected_samples)}")


if __name__ == "__main__":
    UniversityInput.run()
    InterviewInput.run()
    IndustryInput.run()
