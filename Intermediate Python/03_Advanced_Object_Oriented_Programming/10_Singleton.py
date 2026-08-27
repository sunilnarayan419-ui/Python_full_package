from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Any, ClassVar


# ============================================================
# UNIVERSITY LEVEL
# ============================================================
# Goal: understand what "Singleton" literally means -- one shared instance.


class UniLabConfig:
    """Naive Singleton: __new__ ensures only one instance ever exists."""

    _instance: UniLabConfig | None = None

    def __new__(cls) -> UniLabConfig:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.default_units = "ng/uL"
        return cls._instance


class UniversitySingleton:
    @staticmethod
    def run() -> None:
        a = UniLabConfig()
        b = UniLabConfig()
        print("Same instance:", a is b)
        print("Units:", a.default_units)


# ============================================================
# INTERVIEW LEVEL
# ============================================================
# Goal: implement common Singleton approaches and discuss them.


class IvMetaSingleton(type):
    """Metaclass-based Singleton -- reusable across many classes, but
    still carries the same drawbacks as any Singleton (see discussion)."""

    _instances: ClassVar[dict[type, Any]] = {}
    _lock: ClassVar[threading.Lock] = threading.Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class IvInstrumentRegistry(metaclass=IvMetaSingleton):
    def __init__(self) -> None:
        self.registered: list[str] = []

    def register(self, instrument_id: str) -> None:
        self.registered.append(instrument_id)


# --- DISCUSSION ---
# Module-level singleton (Pythonic alternative): a module is only ever
# imported once, so a plain module-level object is already a de facto
# singleton without any special class machinery. This is often preferred
# in Python over __new__/metaclass tricks because it is simpler and more
# explicit. It still shares the fundamental drawback below: any code that
# imports the module can mutate shared state invisibly to the rest of the
# program, which is exactly why the Industry section treats Singleton
# with caution rather than using it by default.


class InterviewSingleton:
    @staticmethod
    def run() -> None:
        registry_a = IvInstrumentRegistry()
        registry_b = IvInstrumentRegistry()
        registry_a.register("INS-01")

        print("Same instance:", registry_a is registry_b)
        print("Visible from b:", registry_b.registered)  # hidden global coupling


# ============================================================
# INDUSTRY LEVEL
# ============================================================
# Goal: demonstrate senior judgment about Singleton -- when it is
# justified, when it is a trap, and what to prefer instead.
#
# ARCHITECTURAL DISTINCTION
# -------------------------
# 1. Global variable: a bare module-level mutable object. Any code can
#    read AND write it from anywhere, with no lifecycle control and no
#    way to substitute a different instance for testing. Avoid this.
#
# 2. Singleton pattern: enforces "exactly one instance can ever exist"
#    at the language/class level. This still creates hidden coupling --
#    any class that references the Singleton by name is secretly
#    depending on global state, even though its constructor signature
#    doesn't show it. Tests become hard to isolate because state can
#    leak between them unless the singleton is explicitly reset.
#
# 3. Dependency-managed shared instance: a single instance is created
#    once (e.g. in a composition root) and then EXPLICITLY passed to
#    everything that needs it via constructor injection. Sharing is
#    still achieved (one object, one identity, no duplication) but
#    without hidden global access -- dependencies stay visible in
#    constructor signatures, and tests can inject a fresh instance or
#    a fake with zero global cleanup.
#
# CONCLUSION: for genuinely immutable, read-only configuration, a
# Singleton-like guarantee is reasonable because there is no mutable
# state to leak. For anything with mutable state (registries, caches,
# connections), prefer the dependency-managed shared instance instead.


class ConfigurationError(ValueError):
    """Raised when lab configuration is constructed with invalid values."""


@dataclass(frozen=True, slots=True)
class LabConfiguration:
    """Immutable value object -- safe to share because it cannot mutate
    after construction, which removes the main risk that makes Singleton
    problematic elsewhere in this file."""

    institution: str
    default_units: str
    max_concurrent_assays: int

    def __post_init__(self) -> None:
        if self.max_concurrent_assays <= 0:
            raise ConfigurationError("max_concurrent_assays must be positive")


class LabConfigurationProvider:
    """Justified, carefully-scoped Singleton-like accessor.

    Justification: application configuration is read extremely often,
    is immutable once loaded, and genuinely represents one process-wide
    truth (there is only one lab this process is running for). Because
    LabConfiguration is frozen, there is no hidden-mutable-state risk.

    This is still built as an explicit, resettable class (not a bare
    module global) so tests can call `reset()` and inject a different
    configuration, avoiding the test-isolation trap of naive Singletons.
    """

    _instance: LabConfiguration | None = None
    _lock: ClassVar[threading.Lock] = threading.Lock()

    @classmethod
    def initialize(cls, config: LabConfiguration) -> None:
        with cls._lock:
            cls._instance = config

    @classmethod
    def get(cls) -> LabConfiguration:
        if cls._instance is None:
            raise ConfigurationError("LabConfigurationProvider not initialized")
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Exists specifically so tests can isolate themselves from
        state left behind by other tests -- a mitigation for the
        Singleton test-isolation problem, not a full solution to it."""
        with cls._lock:
            cls._instance = None


@dataclass
class AssayScheduler:
    """PREFERRED alternative for anything with mutable, per-run state:
    a dependency-managed shared instance, passed explicitly rather than
    looked up globally. Two schedulers can coexist (e.g. one per lab
    site) without any hidden coupling."""

    max_concurrent_assays: int
    active_assays: list[str] = field(default_factory=list)

    def schedule(self, sample_id: str) -> None:
        if len(self.active_assays) >= self.max_concurrent_assays:
            raise ConfigurationError("No capacity to schedule another assay")
        self.active_assays.append(sample_id)


class IndustrySingleton:
    @staticmethod
    def run() -> None:
        LabConfigurationProvider.initialize(
            LabConfiguration("IISc Biotech Lab", "ng/uL", max_concurrent_assays=2)
        )
        config = LabConfigurationProvider.get()
        print(f"Shared config: {config.institution} ({config.default_units})")

        # Mutable state uses explicit sharing instead of a Singleton:
        scheduler = AssayScheduler(max_concurrent_assays=config.max_concurrent_assays)
        scheduler.schedule("S-1")
        scheduler.schedule("S-2")
        try:
            scheduler.schedule("S-3")
        except ConfigurationError as exc:
            print("Rejected:", exc)

        LabConfigurationProvider.reset()  # clean state for the next test/run


if __name__ == "__main__":
    UniversitySingleton.run()
    InterviewSingleton.run()
    IndustrySingleton.run()
