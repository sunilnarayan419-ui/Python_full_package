"""range() for indexed scientific iteration."""


class SampleNumberer:
    def __init__(self, n: int) -> None:
        self.n = n

    def labels(self) -> list[str]:
        result: list[str] = []
        for i in range(self.n):
            result.append(f"sample_{i + 1}")
        return result


class ChromosomeWindow:
    def __init__(self, start: int, stop: int) -> None:
        self.start = start
        self.stop = stop

    def positions(self) -> list[int]:
        return list(range(self.start, self.stop))


class SteppedSequence:
    def __init__(self, length: int, step: int) -> None:
        self.length = length
        self.step = step

    def positions(self) -> list[int]:
        return list(range(0, self.length, self.step))


if __name__ == "__main__":
    print(SampleNumberer(3).labels())

    print(ChromosomeWindow(100, 105).positions())

    print(SteppedSequence(20, 5).positions())
