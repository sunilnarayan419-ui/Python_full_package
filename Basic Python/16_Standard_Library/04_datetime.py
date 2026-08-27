"""Demonstrates the datetime module using laboratory scheduling examples."""

from datetime import date, datetime, timedelta, timezone


class UniversityDateTime:
    """Introduces creating and formatting dates for sample collection records."""

    def __init__(self, collection_date: date) -> None:
        self.collection_date = collection_date

    def format_for_report(self) -> str:
        return self.collection_date.strftime("%B %d, %Y")

    def days_since_collection(self, reference: date) -> int:
        return (reference - self.collection_date).days

    @staticmethod
    def run() -> None:
        collected = date(2026, 5, 10)
        record = UniversityDateTime(collected)

        today = date(2026, 5, 24)
        print(f"Sample collected on: {record.format_for_report()}")
        print(f"Days since collection: {record.days_since_collection(today)}")


class InterviewDateTime:
    """Solves an experiment-duration calculation problem, with edge cases."""

    def calculate_duration(self, start: datetime, end: datetime) -> timedelta:
        """Return the duration between two experiment timestamps.

        Raises ValueError if the end time precedes the start time, since a
        negative experiment duration indicates invalid input.
        """
        if end < start:
            raise ValueError("end must not be earlier than start.")
        return end - start

    def format_duration(self, duration: timedelta) -> str:
        total_minutes = int(duration.total_seconds() // 60)
        hours, minutes = divmod(total_minutes, 60)
        return f"{hours}h {minutes}m"

    def next_business_day(self, current: date) -> date:
        """Return the next weekday, skipping Saturday and Sunday."""
        next_day = current + timedelta(days=1)
        while next_day.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
            next_day += timedelta(days=1)
        return next_day

    @staticmethod
    def run() -> None:
        solver = InterviewDateTime()

        # Test case 1: normal duration
        start = datetime(2026, 5, 10, 9, 0)
        end = datetime(2026, 5, 10, 14, 45)
        duration = solver.calculate_duration(start, end)
        print(f"Experiment duration: {solver.format_duration(duration)}")

        # Test case 2: edge case, invalid ordering
        try:
            solver.calculate_duration(end, start)
        except ValueError as error:
            print(f"Handled invalid duration: {error}")

        friday = date(2026, 5, 15)
        print(f"Next processing day after Friday: {solver.next_business_day(friday)}")


class IndustryDateTime:
    """Timezone-aware scheduling utility for distributed laboratory operations."""

    def __init__(self, lab_timezone: timezone = timezone.utc) -> None:
        self.lab_timezone = lab_timezone

    def schedule_experiment(self, start_local: datetime, duration_hours: float) -> dict[str, str]:
        """Schedule an experiment window, attaching timezone metadata explicitly.

        Timezone-aware datetimes are used because experiment logs are aggregated
        across labs in different regions, where naive datetimes would be ambiguous.
        """
        if start_local.tzinfo is None:
            start_local = start_local.replace(tzinfo=self.lab_timezone)

        end_local = start_local + timedelta(hours=duration_hours)

        return {
            "start": start_local.isoformat(),
            "end": end_local.isoformat(),
            "timezone": str(self.lab_timezone),
        }

    def parse_experiment_timestamp(self, iso_timestamp: str) -> datetime:
        """Parse an ISO-8601 timestamp, raising a clear error on malformed input."""
        try:
            return datetime.fromisoformat(iso_timestamp)
        except ValueError as error:
            raise ValueError(f"Invalid ISO timestamp '{iso_timestamp}': {error}") from error

    @staticmethod
    def run() -> None:
        scheduler = IndustryDateTime(lab_timezone=timezone.utc)

        window = scheduler.schedule_experiment(
            start_local=datetime(2026, 6, 1, 8, 30), duration_hours=3.5
        )
        print("Scheduled experiment window:", window)

        parsed = scheduler.parse_experiment_timestamp(window["start"])
        print(f"Parsed start timestamp: {parsed}")


if __name__ == "__main__":
    UniversityDateTime.run()
    InterviewDateTime.run()
    IndustryDateTime.run()
