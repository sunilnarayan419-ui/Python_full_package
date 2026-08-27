from __future__ import annotations

from dataclasses import dataclass, field


class UniversityHashTable:
    """Uses a Python dict to demonstrate key-value hashing concepts
    with gene symbol -> chromosome mappings."""

    def __init__(self) -> None:
        self.gene_to_chromosome: dict[str, str] = {}

    def insert(self, gene_symbol: str, chromosome: str) -> None:
        """Time: O(1) average, Space: O(1)."""
        self.gene_to_chromosome[gene_symbol] = chromosome

    def lookup(self, gene_symbol: str) -> str | None:
        """Time: O(1) average, Space: O(1)."""
        return self.gene_to_chromosome.get(gene_symbol)

    def delete(self, gene_symbol: str) -> bool:
        """Time: O(1) average, Space: O(1)."""
        if gene_symbol in self.gene_to_chromosome:
            del self.gene_to_chromosome[gene_symbol]
            return True
        return False

    @staticmethod
    def run() -> None:
        table = UniversityHashTable()
        table.insert("TP53", "17")
        table.insert("BRCA1", "17")
        table.insert("EGFR", "7")
        print("University: lookup BRCA1 ->", table.lookup("BRCA1"))
        print("University: lookup unknown ->", table.lookup("XYZ1"))
        table.delete("EGFR")
        print("University: after delete ->", table.gene_to_chromosome)


@dataclass
class _Entry:
    key: str
    value: str


class InterviewHashTable:
    """Simulates hash-table internals with explicit collision handling
    via separate chaining, applied to compound ID -> target protein
    lookups. Demonstrates why average-case lookup is O(1) while
    worst-case (many collisions) degrades to O(n).
    """

    def __init__(self, bucket_count: int = 8) -> None:
        if bucket_count <= 0:
            raise ValueError("bucket_count must be positive")
        self._bucket_count = bucket_count
        self._buckets: list[list[_Entry]] = [[] for _ in range(bucket_count)]
        self._size = 0

    def _hash(self, key: str) -> int:
        """Map a key to a bucket index using Python's built-in hash.

        Time: O(len(key)), Space: O(1)
        """
        return hash(key) % self._bucket_count

    def insert(self, key: str, value: str) -> None:
        """Time: O(1) average, O(bucket size) worst case due to collisions.
        Space: O(1) amortized per insertion.
        """
        if not key:
            raise ValueError("key must not be empty")
        bucket = self._buckets[self._hash(key)]
        for entry in bucket:
            if entry.key == key:
                entry.value = value
                return
        bucket.append(_Entry(key, value))
        self._size += 1

    def lookup(self, key: str) -> str | None:
        """Time: O(1) average, O(bucket size) worst case. Space: O(1)."""
        bucket = self._buckets[self._hash(key)]
        for entry in bucket:
            if entry.key == key:
                return entry.value
        return None

    def delete(self, key: str) -> bool:
        """Time: O(1) average, O(bucket size) worst case. Space: O(1)."""
        bucket = self._buckets[self._hash(key)]
        for index, entry in enumerate(bucket):
            if entry.key == key:
                bucket.pop(index)
                self._size -= 1
                return True
        return False

    def load_factor(self) -> float:
        """Ratio of stored entries to bucket count; a signal for when
        to resize to preserve O(1) average performance.

        Time: O(1), Space: O(1)
        """
        return self._size / self._bucket_count

    @staticmethod
    def run() -> None:
        table = InterviewHashTable(bucket_count=4)
        table.insert("CMPD-001", "EGFR")
        table.insert("CMPD-002", "BRAF")
        table.insert("CMPD-003", "ALK")
        print("Interview: lookup CMPD-002 ->", table.lookup("CMPD-002"))
        print("Interview: load factor ->", table.load_factor())
        deleted = table.delete("CMPD-001")
        print("Interview: deleted CMPD-001 ->", deleted)
        print("Interview: lookup deleted key ->", table.lookup("CMPD-001"))


@dataclass(slots=True)
class ScientificRecord:
    identifier: str
    category: str
    attributes: dict[str, str] = field(default_factory=dict)


class DuplicateIdentifierError(Exception):
    """Raised when inserting an identifier that already exists."""


class IndustryHashTable:
    """A reusable indexed lookup component for scientific identifiers
    (sample IDs, gene IDs, compound IDs, experiment IDs), built on top
    of Python's production-grade dict rather than reimplementing hash
    table internals - dict already provides amortized O(1) operations.
    """

    def __init__(self) -> None:
        self._index: dict[str, ScientificRecord] = {}

    def register(self, record: ScientificRecord, *, allow_overwrite: bool = False) -> None:
        """Register a record under its identifier.

        Time: O(1) average, Space: O(1)
        Raises DuplicateIdentifierError if the identifier exists and
        allow_overwrite is False.
        """
        if not allow_overwrite and record.identifier in self._index:
            raise DuplicateIdentifierError(f"identifier already registered: {record.identifier}")
        self._index[record.identifier] = record

    def get(self, identifier: str) -> ScientificRecord | None:
        """Time: O(1) average, Space: O(1)."""
        return self._index.get(identifier)

    def remove(self, identifier: str) -> bool:
        """Time: O(1) average, Space: O(1)."""
        return self._index.pop(identifier, None) is not None

    def all_in_category(self, category: str) -> list[ScientificRecord]:
        """Time: O(n) - a full scan is required since the index is keyed
        by identifier, not category.
        Space: O(k) for k matches.
        """
        return [record for record in self._index.values() if record.category == category]

    def __len__(self) -> int:
        return len(self._index)

    @staticmethod
    def run() -> None:
        registry = IndustryHashTable()
        registry.register(ScientificRecord("GENE-TP53", "gene", {"chromosome": "17"}))
        registry.register(ScientificRecord("GENE-BRCA1", "gene", {"chromosome": "17"}))
        registry.register(ScientificRecord("CMPD-4471", "compound", {"target": "EGFR"}))

        found = registry.get("GENE-BRCA1")
        print("Industry: found ->", found)

        try:
            registry.register(ScientificRecord("GENE-TP53", "gene", {}))
        except DuplicateIdentifierError as error:
            print("Industry: duplicate caught ->", error)

        genes = registry.all_in_category("gene")
        print("Industry: registered genes ->", [g.identifier for g in genes])
        print("Industry: total records ->", len(registry))


if __name__ == "__main__":
    UniversityHashTable.run()
    InterviewHashTable.run()
    IndustryHashTable.run()
