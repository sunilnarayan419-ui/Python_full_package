from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable


# ============================================================
# UNIVERSITY LEVEL
# ============================================================
# Goal: understand that Protocol gives Python structural ("duck-typed")
# interfaces without requiring explicit inheritance.


@runtime_checkable
class UniMeasurable(Protocol):
    def measure(self) -> float: ...


class UniThermometer:
    """No inheritance from UniMeasurable required -- it satisfies the
    Protocol structurally simply by having a matching measure() method."""

    def measure(self) -> float:
        return 36.6


class UniversityInterfaces:
    @staticmethod
    def run() -> None:
        device: UniMeasurable = UniThermometer()
        print("Is UniMeasurable:", isinstance(device, UniMeasurable))
        print("Measurement:", device.measure())


# ============================================================
# INTERVIEW LEVEL
# ============================================================
# Goal: multiple interchangeable implementations of the same interface,
# selected without the caller knowing concrete types.


class IvGeneRepository(Protocol):
    def get_sequence(self, gene_id: str) -> str: ...


class IvInMemoryGeneRepository:
    def __init__(self, sequences: dict[str, str]) -> None:
        self._sequences = sequences

    def get_sequence(self, gene_id: str) -> str:
        return self._sequences.get(gene_id, "")


class IvReversedGeneRepository:
    """A different storage/transform strategy, same interface."""

    def __init__(self, sequences: dict[str, str]) -> None:
        self._sequences = sequences

    def get_sequence(self, gene_id: str) -> str:
        return self._sequences.get(gene_id, "")[::-1]


def print_gene(repository: IvGeneRepository, gene_id: str) -> None:
    """Depends only on the Protocol -- works with any conforming repository."""
    print(f"{gene_id}: {repository.get_sequence(gene_id)}")


class InterviewInterfaces:
    @staticmethod
    def run() -> None:
        data = {"BRCA1": "ATGCGT"}
        repositories: list[IvGeneRepository] = [
            IvInMemoryGeneRepository(data),
            IvReversedGeneRepository(data),
        ]
        for repo in repositories:
            print_gene(repo, "BRCA1")


# ============================================================
# INDUSTRY LEVEL
# ============================================================
# Goal: interface-driven scientific services with several genuinely
# distinct SequenceRepository implementations. Network dependencies are
# simulated in-process to keep the example self-contained and runnable.


class SequenceNotFoundError(KeyError):
    """Raised when a requested sequence does not exist in the backing store."""


@runtime_checkable
class SequenceRepository(Protocol):
    """The single contract every storage backend must satisfy."""

    def get_sequence(self, sequence_id: str) -> str: ...

    def has_sequence(self, sequence_id: str) -> bool: ...


class InMemorySequenceRepository:
    """Fast, ephemeral storage -- ideal for unit tests."""

    def __init__(self, sequences: dict[str, str] | None = None) -> None:
        self._sequences: dict[str, str] = dict(sequences or {})

    def get_sequence(self, sequence_id: str) -> str:
        if sequence_id not in self._sequences:
            raise SequenceNotFoundError(sequence_id)
        return self._sequences[sequence_id]

    def has_sequence(self, sequence_id: str) -> bool:
        return sequence_id in self._sequences


class FileSequenceRepository:
    """Simulates a file-backed store using an in-process dict as the
    'file system' so the example stays dependency-free and deterministic,
    while still demonstrating a genuinely different storage strategy
    (e.g. lazy-loading, path-keyed lookup) than InMemorySequenceRepository.
    """

    def __init__(self, file_index: dict[str, str]) -> None:
        self._file_index = file_index  # sequence_id -> "file contents"

    def get_sequence(self, sequence_id: str) -> str:
        if sequence_id not in self._file_index:
            raise SequenceNotFoundError(sequence_id)
        return self._file_index[sequence_id].strip()

    def has_sequence(self, sequence_id: str) -> bool:
        return sequence_id in self._file_index


class CachedRemoteSequenceRepository:
    """Simulates a remote repository with a local cache layer, without
    performing real network I/O -- 'remote_lookup' stands in for what
    would otherwise be an HTTP/gRPC call."""

    def __init__(self, remote_lookup: dict[str, str]) -> None:
        self._remote_lookup = remote_lookup
        self._cache: dict[str, str] = {}

    def get_sequence(self, sequence_id: str) -> str:
        if sequence_id in self._cache:
            return self._cache[sequence_id]
        if sequence_id not in self._remote_lookup:
            raise SequenceNotFoundError(sequence_id)
        value = self._remote_lookup[sequence_id]
        self._cache[sequence_id] = value
        return value

    def has_sequence(self, sequence_id: str) -> bool:
        return sequence_id in self._cache or sequence_id in self._remote_lookup


@dataclass
class SequenceLookupService:
    """Depends only on the SequenceRepository Protocol.

    Any conforming backend -- in-memory, file-backed, or remote-with-cache
    -- can be substituted without changing this service, satisfying both
    dependency inversion and interface segregation (clients never see
    storage-specific methods that aren't part of the shared contract).
    """

    repository: SequenceRepository
    lookups_performed: int = field(default=0, init=False)

    def lookup(self, sequence_id: str) -> str:
        self.lookups_performed += 1
        return self.repository.get_sequence(sequence_id)


class IndustryInterfaces:
    @staticmethod
    def run() -> None:
        backends: list[SequenceRepository] = [
            InMemorySequenceRepository({"GENE-1": "ATGCGT"}),
            FileSequenceRepository({"GENE-1": "ATGCGT\n"}),
            CachedRemoteSequenceRepository({"GENE-1": "ATGCGT"}),
        ]

        for backend in backends:
            service = SequenceLookupService(backend)
            print(f"{type(backend).__name__}: {service.lookup('GENE-1')}")

        service = SequenceLookupService(InMemorySequenceRepository())
        try:
            service.lookup("MISSING")
        except SequenceNotFoundError as exc:
            print("Not found:", exc)


if __name__ == "__main__":
    UniversityInterfaces.run()
    InterviewInterfaces.run()
    IndustryInterfaces.run()
