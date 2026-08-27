from __future__ import annotations

import contextlib
import time
from typing import Iterator


class UniversityContextManagers:
    """Demonstrates a basic context manager using __enter__ and __exit__."""

    class ExperimentSession:
        def __init__(self, experiment_name: str) -> None:
            self.experiment_name = experiment_name

        def __enter__(self) -> "UniversityContextManagers.ExperimentSession":
            print(f"starting experiment: {self.experiment_name}")
            return self

        def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> bool:
            print(f"ending experiment: {self.experiment_name}")
            return False

    @staticmethod
    def run() -> None:
        with UniversityContextManagers.ExperimentSession("germination-trial-1") as session:
            print(f"recording data for {session.experiment_name}")


class InterviewContextManagers:
    """Demonstrates a context manager that guarantees resource cleanup even
    when exceptions occur, and one built via contextlib.contextmanager."""

    class SensorConnection:
        def __init__(self, sensor_id: str) -> None:
            self.sensor_id = sensor_id
            self.connected = False

        def __enter__(self) -> "InterviewContextManagers.SensorConnection":
            self.connected = True
            print(f"sensor {self.sensor_id} connected")
            return self

        def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: object) -> bool:
            self.connected = False
            print(f"sensor {self.sensor_id} disconnected")
            if exc_type is not None:
                print(f"handled error during session: {exc_val}")
            return True  # suppress exception after cleanup

    @staticmethod
    @contextlib.contextmanager
    def timed_block(label: str) -> Iterator[None]:
        start = time.perf_counter()
        try:
            yield
        finally:
            elapsed = (time.perf_counter() - start) * 1000
            print(f"[{label}] elapsed {elapsed:.3f} ms")

    @staticmethod
    def run() -> None:
        with InterviewContextManagers.SensorConnection("temp-01") as sensor:
            print(f"reading from {sensor.sensor_id}")
            raise RuntimeError("sensor timeout")

        with InterviewContextManagers.timed_block("batch-processing"):
            sum(i * i for i in range(10_000))


class IndustryContextManagers:
    """Demonstrates a production-style context manager that manages a
    laboratory data-processing session: acquiring a resource, tracking
    state, rolling back on failure, and committing on success."""

    class ProcessingSession:
        """Manages an in-memory transactional batch of sample records,
        committing only if all records process without error."""

        def __init__(self, batch_id: str) -> None:
            self.batch_id = batch_id
            self._committed_records: list[dict[str, float]] = []
            self._pending_records: list[dict[str, float]] = []

        def add_record(self, sample_id: str, concentration: float) -> None:
            if concentration < 0:
                raise ValueError(f"invalid concentration for {sample_id}: {concentration}")
            self._pending_records.append({"sample_id": sample_id, "concentration": concentration})

        def __enter__(self) -> "IndustryContextManagers.ProcessingSession":
            print(f"opening batch {self.batch_id}")
            return self

        def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: object,
        ) -> bool:
            if exc_type is None:
                self._committed_records = list(self._pending_records)
                print(f"batch {self.batch_id} committed with {len(self._committed_records)} records")
            else:
                print(f"batch {self.batch_id} rolled back due to: {exc_val}")
            self._pending_records.clear()
            return False

        @property
        def committed_records(self) -> list[dict[str, float]]:
            return list(self._committed_records)

    @staticmethod
    def run() -> None:
        session = IndustryContextManagers.ProcessingSession("batch-2024-07")
        try:
            with session as active:
                active.add_record("s-001", 4.2)
                active.add_record("s-002", 3.8)
                active.add_record("s-003", -1.0)
        except ValueError as exc:
            print(f"caught expected error: {exc}")

        print(f"records after rollback: {session.committed_records}")

        with IndustryContextManagers.ProcessingSession("batch-2024-08") as active:
            active.add_record("s-101", 5.1)
            active.add_record("s-102", 6.7)

        print(f"records after commit: {active.committed_records}")


if __name__ == "__main__":
    UniversityContextManagers.run()
    InterviewContextManagers.run()
    IndustryContextManagers.run()
