from __future__ import annotations


class UniversityWalrusOperator:
    """Use the walrus operator (:=) in a simple filtering example over
    plant height measurements."""

    @staticmethod
    def filter_tall_plants(heights: list[float], threshold: float) -> list[float]:
        """Assign and test the computed average in a single expression
        using :=, avoiding a separate statement to compute it first.

        Time: O(n)
        """
        tall_plants: list[float] = []
        for height in heights:
            if (excess := height - threshold) > 0:
                tall_plants.append(height)
                print(f"  University: plant exceeds threshold by {excess:.1f} cm")
        return tall_plants

    @staticmethod
    def run() -> None:
        heights = [12.5, 20.1, 9.3, 25.7]
        result = UniversityWalrusOperator.filter_tall_plants(heights, 15.0)
        print("University: tall plants ->", result)


class InterviewWalrusOperator:
    """Demonstrate practical := use inside loops, conditions, and
    comprehensions, over a stream of noisy instrument readings."""

    @staticmethod
    def read_until_stable(raw_readings: list[float | None]) -> list[float]:
        """Consume readings until a None (sentinel for "instrument idle")
        is encountered, using := to fetch-and-check in one step within
        the loop condition.

        Time: O(n)
        """
        collected: list[float] = []
        index = 0
        while index < len(raw_readings) and (current := raw_readings[index]) is not None:
            collected.append(current)
            index += 1
        return collected

    @staticmethod
    def valid_readings_above(raw_readings: list[str], threshold: float) -> list[float]:
        """Use := inside a list comprehension to avoid parsing each
        value twice (once to check validity, once to use it).

        Time: O(n)
        """
        return [
            parsed
            for raw in raw_readings
            if (parsed := InterviewWalrusOperator._safe_parse(raw)) is not None and parsed > threshold
        ]

    @staticmethod
    def _safe_parse(raw: str) -> float | None:
        try:
            return float(raw)
        except ValueError:
            return None

    @staticmethod
    def run() -> None:
        stream: list[float | None] = [1.2, 1.5, 1.9, None, 2.3]
        stable_readings = InterviewWalrusOperator.read_until_stable(stream)
        print("Interview: readings before idle sentinel ->", stable_readings)

        raw_values = ["4.1", "bad", "6.7", "2.0", "not_a_number"]
        above_threshold = InterviewWalrusOperator.valid_readings_above(raw_values, 3.0)
        print("Interview: valid readings above 3.0 ->", above_threshold)


class IndustryWalrusOperator:
    """Uses := selectively where it genuinely improves clarity (avoiding
    a repeated computation), and deliberately uses plain assignment
    everywhere else - readability outranks cleverness in production code.
    """

    @staticmethod
    def summarize_batch(readings: list[float]) -> dict[str, float]:
        """A plain, clear implementation. No walrus operator is used
        here because ordinary assignment is already perfectly readable;
        forcing := in would add no value.

        Time: O(n)
        """
        if not readings:
            return {"count": 0, "mean": 0.0}
        total = sum(readings)
        mean = total / len(readings)
        return {"count": len(readings), "mean": mean}

    @staticmethod
    def find_first_out_of_range(readings: list[float], low: float, high: float) -> float | None:
        """Here := is justified: it lets us test membership in range
        and capture the offending value in one readable expression
        instead of computing it twice or introducing an extra variable
        before the loop body needs it.

        Time: O(n)
        """
        for value in readings:
            if not (low <= (checked := value) <= high):
                return checked
        return None

    @staticmethod
    def run() -> None:
        readings = [36.9, 37.1, 37.0, 41.5, 36.8]
        summary = IndustryWalrusOperator.summarize_batch(readings)
        print("Industry: batch summary (plain assignment used) ->", summary)

        out_of_range = IndustryWalrusOperator.find_first_out_of_range(readings, 36.0, 38.0)
        print("Industry: first out-of-range reading (walrus used) ->", out_of_range)


if __name__ == "__main__":
    UniversityWalrusOperator.run()
    InterviewWalrusOperator.run()
    IndustryWalrusOperator.run()
