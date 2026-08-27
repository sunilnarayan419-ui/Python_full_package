from __future__ import annotations

from collections import deque


class UniversityDeque:
    """Demonstrates collections.deque for efficient appends and pops from
    both ends, contrasted with a plain list."""

    @staticmethod
    def run() -> None:
        sample_queue: deque[str] = deque()
        sample_queue.append("sample-1")
        sample_queue.append("sample-2")
        sample_queue.appendleft("priority-sample")

        print(list(sample_queue))
        processed = sample_queue.popleft()
        print(f"processed: {processed}")
        print(list(sample_queue))


class InterviewDeque:
    """Demonstrates a bounded deque (maxlen) implementing a rolling window,
    a common interview pattern for streaming/sliding-window statistics."""

    class RollingWindow:
        def __init__(self, window_size: int) -> None:
            if window_size <= 0:
                raise ValueError("window_size must be positive")
            self._values: deque[float] = deque(maxlen=window_size)

        def add(self, value: float) -> None:
            self._values.append(value)

        def average(self) -> float:
            return sum(self._values) / len(self._values) if self._values else 0.0

        def is_full(self) -> bool:
            return len(self._values) == self._values.maxlen

    @staticmethod
    def run() -> None:
        window = InterviewDeque.RollingWindow(window_size=3)
        for temperature in (20.1, 21.4, 19.8, 22.5, 23.0):
            window.add(temperature)
            print(f"reading={temperature} rolling_avg={window.average():.2f} full={window.is_full()}")


class IndustryDeque:
    """Demonstrates a deque powering a bounded event buffer for a lab
    monitoring service, supporting efficient two-sided access, snapshotting,
    and threshold-based anomaly retrieval over recent sensor history."""

    class SensorEventBuffer:
        def __init__(self, capacity: int) -> None:
            if capacity <= 0:
                raise ValueError("capacity must be positive")
            self._buffer: deque[tuple[str, float]] = deque(maxlen=capacity)

        def record(self, sensor_id: str, value: float) -> None:
            self._buffer.append((sensor_id, value))

        def recent(self, n: int) -> list[tuple[str, float]]:
            if n <= 0:
                raise ValueError("n must be positive")
            return list(self._buffer)[-n:]

        def anomalies(self, threshold: float) -> list[tuple[str, float]]:
            return [entry for entry in self._buffer if entry[1] > threshold]

        def rotate_oldest_to_review_queue(self, review_queue: "deque[tuple[str, float]]", count: int) -> None:
            """Moves the oldest `count` events out of the live buffer into a
            separate review queue, demonstrating deque.popleft() driven
            data hand-off between pipeline stages."""
            for _ in range(min(count, len(self._buffer))):
                review_queue.append(self._buffer.popleft())

    @staticmethod
    def run() -> None:
        buffer = IndustryDeque.SensorEventBuffer(capacity=5)
        readings = [("co2", 410.0), ("co2", 415.5), ("co2", 620.0), ("co2", 418.2), ("co2", 402.1)]
        for sensor_id, value in readings:
            buffer.record(sensor_id, value)

        print(f"recent 3: {buffer.recent(3)}")
        print(f"anomalies above 500: {buffer.anomalies(500.0)}")

        review_queue: deque[tuple[str, float]] = deque()
        buffer.rotate_oldest_to_review_queue(review_queue, count=2)
        print(f"review queue: {list(review_queue)}")
        print(f"remaining buffer: {buffer.recent(10)}")


if __name__ == "__main__":
    UniversityDeque.run()
    InterviewDeque.run()
    IndustryDeque.run()
