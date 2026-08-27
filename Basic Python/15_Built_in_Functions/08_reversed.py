"""Demonstrations of the built-in reversed() function using experimental sequences."""


class UniversityReversed:
    """Teach the fundamental behavior of reversed() on biological sequences."""

    def __init__(self, dna_sequence: str) -> None:
        self.dna_sequence = dna_sequence

    def reverse_sequence(self) -> str:
        return "".join(reversed(self.dna_sequence))

    @staticmethod
    def run() -> None:
        processor = UniversityReversed(dna_sequence="ATCGGTA")
        print(f"Original sequence: {processor.dna_sequence}")
        print(f"Reversed sequence: {processor.reverse_sequence()}")


class InterviewReversed:
    """Process experimental observations from newest to oldest without copying."""

    def __init__(self, observations: list[dict[str, object]]) -> None:
        self.observations = observations

    def most_recent_first(self) -> list[str]:
        """Iterate observations in reverse (newest last -> newest first)."""
        return [obs["timestamp"] for obs in reversed(self.observations)]

    @staticmethod
    def run() -> None:
        case_one: list[dict[str, object]] = [
            {"timestamp": "day_1", "value": 3.2},
            {"timestamp": "day_2", "value": 3.6},
            {"timestamp": "day_3", "value": 4.1},
        ]
        case_two: list[dict[str, object]] = []

        analyzer_one = InterviewReversed(case_one)
        analyzer_two = InterviewReversed(case_two)

        print(f"Newest-to-oldest order: {analyzer_one.most_recent_first()}")
        print(f"Newest-to-oldest order (empty): {analyzer_two.most_recent_first()}")


class IndustryReversed:
    """Reverse-order processing of scientific data for audit-style workflows."""

    def __init__(self, measurement_log: list[dict[str, object]]) -> None:
        self.measurement_log = measurement_log

    def latest_n_entries(self, count: int) -> list[dict[str, object]]:
        """Return the most recent `count` entries, newest first.

        Uses reversed() as an iterator to avoid copying the entire log,
        then takes only as many entries as requested.
        """
        latest: list[dict[str, object]] = []
        for entry in reversed(self.measurement_log):
            if len(latest) >= count:
                break
            latest.append(entry)
        return latest

    @staticmethod
    def run() -> None:
        measurement_log: list[dict[str, object]] = [
            {"entry_id": "E001", "concentration": 3.1},
            {"entry_id": "E002", "concentration": 3.4},
            {"entry_id": "E003", "concentration": 3.9},
            {"entry_id": "E004", "concentration": 4.2},
            {"entry_id": "E005", "concentration": 4.5},
        ]

        reporter = IndustryReversed(measurement_log)
        latest_entries = reporter.latest_n_entries(2)
        print(f"Two most recent entries: {[e['entry_id'] for e in latest_entries]}")


if __name__ == "__main__":
    UniversityReversed.run()
    InterviewReversed.run()
    IndustryReversed.run()
