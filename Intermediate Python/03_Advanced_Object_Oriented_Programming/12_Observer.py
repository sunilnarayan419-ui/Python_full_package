from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Protocol


# ============================================================
# UNIVERSITY LEVEL
# ============================================================
# Goal: understand the basic publisher/subscriber relationship.


class UniObserver(Protocol):
    def update(self, status: str) -> None: ...


class UniPrintObserver:
    def update(self, status: str) -> None:
        print(f"[observer] status changed to: {status}")


class UniExperiment:
    """Publisher: notifies observers instead of them polling for state."""

    def __init__(self) -> None:
        self._observers: list[UniObserver] = []
        self.status = "created"

    def subscribe(self, observer: UniObserver) -> None:
        self._observers.append(observer)

    def set_status(self, status: str) -> None:
        self.status = status
        for observer in self._observers:
            observer.update(status)


class UniversityObserver:
    @staticmethod
    def run() -> None:
        experiment = UniExperiment()
        experiment.subscribe(UniPrintObserver())
        experiment.set_status("running")
        experiment.set_status("completed")


# ============================================================
# INTERVIEW LEVEL
# ============================================================
# Goal: multiple, independently-acting observers reacting to the same
# scientific event stream.


class IvEventKind(Enum):
    STARTED = auto()
    COMPLETED = auto()
    FAILED = auto()


class IvObserver(Protocol):
    def on_event(self, kind: IvEventKind, experiment_id: str) -> None: ...


class IvLoggingObserver:
    def on_event(self, kind: IvEventKind, experiment_id: str) -> None:
        print(f"[log] {experiment_id}: {kind.name}")


class IvAlertingObserver:
    def on_event(self, kind: IvEventKind, experiment_id: str) -> None:
        if kind is IvEventKind.FAILED:
            print(f"[ALERT] {experiment_id} failed!")


class IvExperimentSubject:
    def __init__(self, experiment_id: str) -> None:
        self.experiment_id = experiment_id
        self._observers: list[IvObserver] = []

    def subscribe(self, observer: IvObserver) -> None:
        self._observers.append(observer)

    def unsubscribe(self, observer: IvObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def emit(self, kind: IvEventKind) -> None:
        for observer in self._observers:
            observer.on_event(kind, self.experiment_id)


class InterviewObserver:
    @staticmethod
    def run() -> None:
        subject = IvExperimentSubject("EXP-200")
        logger = IvLoggingObserver()
        alerter = IvAlertingObserver()

        subject.subscribe(logger)
        subject.subscribe(alerter)

        subject.emit(IvEventKind.STARTED)
        subject.emit(IvEventKind.FAILED)  # both observers react independently

        subject.unsubscribe(alerter)
        subject.emit(IvEventKind.COMPLETED)  # only logger reacts now


# ============================================================
# INDUSTRY LEVEL
# ============================================================
# Goal: a lightweight, self-contained event-driven monitoring model with
# several distinct observers, without a full message broker.


class ExperimentEventKind(Enum):
    STARTED = auto()
    SAMPLE_PROCESSED = auto()
    COMPLETED = auto()
    FAILED = auto()


@dataclass(frozen=True, slots=True)
class ExperimentEvent:
    experiment_id: str
    kind: ExperimentEventKind
    detail: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class ExperimentObserver(Protocol):
    """Narrow contract: observers only need on_event(). The subject never
    knows or cares what each observer does with the event -- this is what
    keeps publisher and subscribers loosely coupled."""

    def on_event(self, event: ExperimentEvent) -> None: ...


class AuditLogger:
    def __init__(self) -> None:
        self.entries: list[str] = []

    def on_event(self, event: ExperimentEvent) -> None:
        self.entries.append(f"{event.timestamp.isoformat()} {event.kind.name} {event.detail}")


class ExperimentReporter:
    def __init__(self) -> None:
        self._processed_samples = 0

    def on_event(self, event: ExperimentEvent) -> None:
        if event.kind is ExperimentEventKind.SAMPLE_PROCESSED:
            self._processed_samples += 1
        if event.kind is ExperimentEventKind.COMPLETED:
            print(
                f"[report] {event.experiment_id} finished, "
                f"{self._processed_samples} samples processed"
            )


class MetricsCollector:
    def __init__(self) -> None:
        self.counts: dict[ExperimentEventKind, int] = {}

    def on_event(self, event: ExperimentEvent) -> None:
        self.counts[event.kind] = self.counts.get(event.kind, 0) + 1


class AlertHandler:
    def on_event(self, event: ExperimentEvent) -> None:
        if event.kind is ExperimentEventKind.FAILED:
            print(f"[ALERT] {event.experiment_id} failed: {event.detail}")


class ExperimentMonitor:
    """Subject: owns the observer list and emits events. Adding a new
    kind of reaction (e.g. a future SlackNotifier) never requires
    modifying ExperimentMonitor -- it only requires a new class that
    implements ExperimentObserver and a subscribe() call, which is the
    concrete payoff of the Observer pattern's loose coupling.
    """

    def __init__(self, experiment_id: str) -> None:
        self.experiment_id = experiment_id
        self._observers: list[ExperimentObserver] = []

    def subscribe(self, observer: ExperimentObserver) -> None:
        self._observers.append(observer)

    def _emit(self, kind: ExperimentEventKind, detail: str) -> None:
        event = ExperimentEvent(self.experiment_id, kind, detail)
        for observer in self._observers:
            observer.on_event(event)

    def start(self) -> None:
        self._emit(ExperimentEventKind.STARTED, "experiment initialized")

    def process_sample(self, sample_id: str) -> None:
        self._emit(ExperimentEventKind.SAMPLE_PROCESSED, sample_id)

    def complete(self) -> None:
        self._emit(ExperimentEventKind.COMPLETED, "all samples processed")

    def fail(self, reason: str) -> None:
        self._emit(ExperimentEventKind.FAILED, reason)


class IndustryObserver:
    @staticmethod
    def run() -> None:
        monitor = ExperimentMonitor("EXP-300")
        audit_logger = AuditLogger()
        metrics = MetricsCollector()

        monitor.subscribe(audit_logger)
        monitor.subscribe(ExperimentReporter())
        monitor.subscribe(metrics)
        monitor.subscribe(AlertHandler())

        monitor.start()
        monitor.process_sample("S-1")
        monitor.process_sample("S-2")
        monitor.complete()

        failing_monitor = ExperimentMonitor("EXP-301")
        failing_monitor.subscribe(AlertHandler())
        failing_monitor.fail("instrument calibration error")

        print("Audit entries:", len(audit_logger.entries))
        print("Metrics:", {k.name: v for k, v in metrics.counts.items()})


if __name__ == "__main__":
    UniversityObserver.run()
    InterviewObserver.run()
    IndustryObserver.run()
