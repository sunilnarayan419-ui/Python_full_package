"""11_Set_Methods.py — Python set methods through plant science and genomics."""
from __future__ import annotations


class PlantGeneSetMethodsUniversity:
    """University level: basic set modification with add, update, remove, discard, pop, clear."""

    def __init__(self) -> None:
        self.genes: set[str] = set()

    def demonstrate(self) -> None:
        self.genes.add("AT1G01010")
        self.genes.update(["AT1G01020", "AT1G01030"])
        print(f"After add/update: {sorted(self.genes)}")
        self.genes.discard("AT1G01099")
        self.genes.remove("AT1G01020")
        print(f"After discard/remove: {sorted(self.genes)}")
        popped = self.genes.pop()
        print(f"After pop() -> {popped}: {sorted(self.genes)}")
        self.genes.clear()
        print(f"After clear: {self.genes}")

    @staticmethod
    def run() -> None:
        demo = PlantGeneSetMethodsUniversity()
        demo.demonstrate()


class IdentifierCleanerInterview:
    """Interview level: update and clean biological identifier collections."""

    def __init__(self, identifiers: set[str]) -> None:
        self.identifiers = identifiers

    def add_batch(self, new_ids: list[str]) -> None:
        self.identifiers.update(new_ids)

    def remove_if_present(self, target: str) -> bool:
        if target in self.identifiers:
            self.identifiers.remove(target)
            return True
        return False

    def safe_remove(self, target: str) -> None:
        self.identifiers.discard(target)

    @staticmethod
    def run() -> None:
        ids = {"AT1G01010", "AT1G01020", "AT1G01030"}
        cleaner = IdentifierCleanerInterview(ids)
        cleaner.add_batch(["AT1G01040", "AT1G01050"])
        found = cleaner.remove_if_present("AT1G01020")
        cleaner.safe_remove("AT1G01099")
        print("Interview — Cleaned identifiers:")
        print(f"  Removed AT1G01020 found={found}")
        print(f"  Remaining: {sorted(cleaner.identifiers)}")


class GenomicIdentifierManagerIndustry:
    """Industry level: genomic identifier management with error handling."""

    def __init__(self) -> None:
        self.primary: set[str] = set()
        self.backup: set[str] = set()

    def register_primary(self, gene_id: str) -> None:
        if not gene_id or not isinstance(gene_id, str):
            raise ValueError("gene_id must be a non-empty string")
        self.primary.add(gene_id)

    def promote_from_backup(self, gene_id: str) -> None:
        if gene_id in self.backup:
            self.backup.remove(gene_id)
            self.primary.add(gene_id)
        else:
            raise KeyError(f"{gene_id} not in backup set")

    def archive_primary(self, gene_id: str) -> None:
        if gene_id in self.primary:
            self.primary.discard(gene_id)
            self.backup.add(gene_id)

    def purge_backup(self) -> None:
        self.backup.clear()

    @staticmethod
    def run() -> None:
        manager = GenomicIdentifierManagerIndustry()
        for gid in ["AT1G01010", "AT1G01020", "AT1G01030"]:
            manager.register_primary(gid)
        manager.archive_primary("AT1G01020")
        manager.promote_from_backup("AT1G01020")
        manager.purge_backup()
        print("Industry — Identifier manager state:")
        print(f"  Primary: {sorted(manager.primary)}")
        print(f"  Backup:  {sorted(manager.backup)}")


if __name__ == "__main__":
    PlantGeneSetMethodsUniversity.run()
    print()
    IdentifierCleanerInterview.run()
    print()
    GenomicIdentifierManagerIndustry.run()