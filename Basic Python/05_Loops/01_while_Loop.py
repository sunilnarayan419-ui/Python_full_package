"""while loop in scientific data processing."""


class GrowthSimulator:
    def __init__(self, initial_cm: float, rate_cm_per_day: float) -> None:
        self.height = initial_cm
        self.rate = rate_cm_per_day

    def days_to_reach(self, target_cm: float) -> int:
        days = 0
        while self.height < target_cm:
            self.height += self.rate
            days += 1
        return days


class SequenceScanner:
    def __init__(self, sequence: str) -> None:
        self.sequence = sequence.upper()

    def scan_until_stop(self) -> int:
        i = 0
        while i < len(self.sequence) and self.sequence[i] != "N":
            i += 1
        return i


class ExperimentalRunner:
    def __init__(self, replicate: int) -> None:
        self.replicate = replicate
        self.results: list[int] = []

    def run_until_threshold(self, threshold: int) -> int:
        count = 0
        while count < threshold:
            count += 1
            self.results.append(count * self.replicate)
        return count


if __name__ == "__main__":
    print(GrowthSimulator(10.0, 2.0).days_to_reach(20.0))

    print(SequenceScanner("ATGCNAT").scan_until_stop())

    print(ExperimentalRunner(replicate=5).run_until_threshold(3))
