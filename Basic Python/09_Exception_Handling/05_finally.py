"""The finally clause: guaranteed cleanup, and when a context manager is preferable."""

from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass, field


class UniversityFinally:
    """Demonstrates that finally always executes, regardless of success or failure."""

    @staticmethod
    def process_reading(raw_value: str) -> None:
        print("Starting measurement processing...")
        try:
            reading = float(raw_value)
            print(f"Processed reading: {reading}")
        except ValueError:
            print(f"Invalid reading skipped: {raw_value!r}")
        finally:
            print("Measurement processing complete.")

    @staticmethod
    def run() -> None:
        print("--- UniversityFinally ---")
        UniversityFinally.process_reading("21.6")
        UniversityFinally.process_reading("unreadable")


class InterviewFinally:
    """Demonstrates cleanup of a simulated laboratory resource using finally."""

    @staticmethod
    def run_lab_instrument_session(sample_ids: list[str]) -> None:
        instrument_locked = False
        try:
            instrument_locked = True
            print("Instrument locked for exclusive use.")
            for sample_id in sample_ids:
                if sample_id == "":
                    raise ValueError("Empty sample id cannot be processed")
                print(f"Measuring sample: {sample_id}")
        except ValueError as exc:
            print(f"Session aborted: {exc}")
        finally:
            if instrument_locked:
                instrument_locked = False
                print("Instrument released.")

    @staticmethod
    def run() -> None:
        print("--- InterviewFinally ---")
        InterviewFinally.run_lab_instrument_session(["S001", "S002"])
        InterviewFinally.run_lab_instrument_session(["S003", "", "S004"])


@dataclass
class TemperatureLogWriter:
    path: str
    _handle: object | None = field(default=None, init=False)

    def __enter__(self) -> "TemperatureLogWriter":
        self._handle = open(self.path, "w", encoding="utf-8")
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        if self._handle is not None:
            self._handle.close()
        return False

    def write_reading(self, sample_id: str, temperature_c: float) -> None:
        assert self._handle is not None
        self._handle.write(f"{sample_id},{temperature_c}\n")


class IndustryFinally:
    """Demonstrates preferring a context manager over manual finally-based cleanup."""

    @staticmethod
    def write_temperature_log(readings: list[tuple[str, float]], path: str) -> None:
        with TemperatureLogWriter(path) as writer:
            for sample_id, temperature_c in readings:
                if temperature_c < -273.15:
                    raise ValueError(
                        f"Impossible temperature for {sample_id}: {temperature_c}"
                    )
                writer.write_reading(sample_id, temperature_c)

    @staticmethod
    def run() -> None:
        print("--- IndustryFinally ---")
        temp_path = os.path.join(tempfile.gettempdir(), "temperature_log_demo.csv")
        try:
            IndustryFinally.write_temperature_log(
                [("T001", 22.4), ("T002", 19.8)], temp_path
            )
            print(f"Temperature log written successfully to {temp_path}")
        except ValueError as exc:
            print(f"Failed to write temperature log: {exc}")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
                print("Temporary temperature log file removed.")


if __name__ == "__main__":
    UniversityFinally.run()
    InterviewFinally.run()
    IndustryFinally.run()
