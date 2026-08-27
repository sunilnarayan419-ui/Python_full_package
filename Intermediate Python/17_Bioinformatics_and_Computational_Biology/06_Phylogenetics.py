from __future__ import annotations

from io import StringIO

from Bio import Phylo
from Bio.Align import MultipleSeqAlignment
from Bio.Phylo.BaseTree import Clade, Tree
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

# Small, deterministic pre-aligned ortholog fragment set (illustrative
# computational workflow only, not a real evolutionary study).
_ALIGNED_SEQUENCES: dict[str, str] = {
    "Homo_sapiens_TP53": "MEEPQSDPSVEPPLSQETFSDLWKLLPENN",
    "Pan_troglodytes_TP53": "MEEPQSDPSVEPPLSQETFSDLWKLLPENS",
    "Mus_musculus_Tp53": "MEETFSGLWKLLPENNVLSTLPSSDSIEEW",
    "Gallus_gallus_TP53": "MEEPQSDLSIEPPLSQETFADLWKLLPENN",
}


class PhylogeneticsWorkflow:
    """Industry-level phylogenetics workflow using Bio.Align and Bio.Phylo.

    Builds a distance-based phylogenetic tree from a small deterministic
    pre-aligned sequence set and exposes clade traversal, Newick export,
    and basic topology inspection utilities.
    """

    def __init__(self, aligned_sequences: dict[str, str]) -> None:
        """Initialize with a mapping of taxon label -> aligned sequence.

        Args:
            aligned_sequences: Pre-aligned sequences, all of equal length.
        """
        if not self.validate_alignment(aligned_sequences):
            raise ValueError("All aligned sequences must be non-empty and equal length")
        self.taxon_labels = list(aligned_sequences.keys())
        self.alignment: MultipleSeqAlignment = MultipleSeqAlignment(
            [
                SeqRecord(Seq(sequence), id=label, description="")
                for label, sequence in aligned_sequences.items()
            ]
        )
        self.tree: Tree | None = None

    @staticmethod
    def validate_alignment(aligned_sequences: dict[str, str]) -> bool:
        """Validate non-empty, equal-length aligned sequences."""
        if not aligned_sequences:
            return False
        lengths = {len(seq) for seq in aligned_sequences.values() if seq}
        return len(lengths) == 1 and all(seq for seq in aligned_sequences.values())

    def build_distance_tree(self, model: str = "identity", method: str = "nj") -> Tree:
        """Construct a phylogenetic tree using a distance-based method.

        Args:
            model: Substitution/distance model passed to DistanceCalculator
                (e.g. "identity", "blosum62").
            method: Tree-building method, "nj" (neighbor-joining) or "upgma".
        """
        calculator = DistanceCalculator(model)
        distance_matrix = calculator.get_distance(self.alignment)

        constructor = DistanceTreeConstructor(calculator)
        if method == "nj":
            self.tree = constructor.nj(distance_matrix)
        elif method == "upgma":
            self.tree = constructor.upgma(distance_matrix)
        else:
            raise ValueError(f"Unsupported tree construction method: {method}")
        return self.tree

    def traverse_clades(self) -> list[str]:
        """Return terminal (leaf) clade names in tree traversal order."""
        if self.tree is None:
            raise RuntimeError("Tree has not been built; call build_distance_tree first")
        return [clade.name for clade in self.tree.get_terminals() if clade.name]

    def tree_metadata(self) -> dict[str, int | float]:
        """Compute basic topology metadata: terminal/internal clade counts and depth."""
        if self.tree is None:
            raise RuntimeError("Tree has not been built; call build_distance_tree first")
        terminals = self.tree.get_terminals()
        internals = self.tree.get_nonterminals()
        depths = self.tree.depths()
        max_depth = max(depths.values()) if depths else 0.0
        return {
            "terminal_count": len(terminals),
            "internal_node_count": len(internals),
            "max_branch_depth": round(float(max_depth), 4),
        }

    def to_newick(self) -> str:
        """Serialize the constructed tree to Newick format."""
        if self.tree is None:
            raise RuntimeError("Tree has not been built; call build_distance_tree first")
        buffer = StringIO()
        Phylo.write(self.tree, buffer, "newick")
        return buffer.getvalue().strip()

    def find_clade_by_name(self, name: str) -> Clade | None:
        """Locate a terminal clade by exact taxon label.

        Args:
            name: Taxon label to search for among terminal clades.
        """
        if self.tree is None:
            raise RuntimeError("Tree has not been built; call build_distance_tree first")
        matches = self.tree.find_clades(name=name, terminal=True)
        return next(matches, None)

    @staticmethod
    def run() -> None:
        """Demonstrate alignment loading, tree construction, and inspection."""
        workflow = PhylogeneticsWorkflow(_ALIGNED_SEQUENCES)
        print(f"Loaded alignment with {len(workflow.taxon_labels)} taxa: {workflow.taxon_labels}")

        tree = workflow.build_distance_tree(model="identity", method="nj")
        print(f"Constructed tree with root: {tree.root}")

        print("Terminal clades in traversal order:", workflow.traverse_clades())
        print("Tree metadata:", workflow.tree_metadata())
        print("Newick representation:")
        print(workflow.to_newick())

        clade = workflow.find_clade_by_name("Homo_sapiens_TP53")
        if clade is not None:
            print(f"Found clade for Homo_sapiens_TP53 with branch length {clade.branch_length}")


if __name__ == "__main__":
    PhylogeneticsWorkflow.run()
