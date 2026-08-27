from __future__ import annotations

from dataclasses import dataclass

from Bio.SeqUtils.ProtParam import ProteinAnalysis

_VALID_AMINO_ACIDS = frozenset("ACDEFGHIKLMNPQRSTVWY")


@dataclass
class ProteinPropertyReport:
    """Structured physicochemical property report for a single protein."""

    identifier: str
    length: int
    molecular_weight: float
    aromaticity: float
    instability_index: float
    isoelectric_point: float
    gravy: float
    helix_fraction: float
    turn_fraction: float
    sheet_fraction: float
    amino_acid_composition: dict[str, float]


class ProteinAnalysisWorkflow:
    """Industry-level protein sequence analysis workflow using Bio.SeqUtils.

    Computes standard physicochemical descriptors used in early-stage
    protein characterization and drug-target triage. Results are
    computational descriptors only, not functional or clinical claims.
    """

    def __init__(self, sequence: str, identifier: str) -> None:
        """Initialize with a raw protein sequence and identifier.

        Args:
            sequence: Amino-acid sequence, standard one-letter codes only.
            identifier: Local label such as a UniProt-style accession.
        """
        cleaned = sequence.strip().upper()
        if not self.validate_sequence(cleaned):
            raise ValueError("Sequence contains non-standard amino-acid symbols")
        self.identifier = identifier
        self.sequence = cleaned
        self._analyzer = ProteinAnalysis(self.sequence)

    @staticmethod
    def validate_sequence(sequence: str) -> bool:
        """Validate that a sequence is non-empty and uses only the 20 standard amino acids."""
        return bool(sequence) and set(sequence).issubset(_VALID_AMINO_ACIDS)

    def amino_acid_composition(self) -> dict[str, float]:
        """Return the percentage composition of each amino acid present."""
        composition = self._analyzer.amino_acids_percent
        return {aa: round(fraction * 100.0, 2) for aa, fraction in composition.items()}

    def secondary_structure_fraction(self) -> dict[str, float]:
        """Return predicted helix/turn/sheet propensity fractions."""
        helix, turn, sheet = self._analyzer.secondary_structure_fraction()
        return {
            "helix_fraction": round(helix, 4),
            "turn_fraction": round(turn, 4),
            "sheet_fraction": round(sheet, 4),
        }

    def generate_report(self) -> ProteinPropertyReport:
        """Compute a full structured physicochemical property report."""
        ss_fractions = self.secondary_structure_fraction()
        return ProteinPropertyReport(
            identifier=self.identifier,
            length=len(self.sequence),
            molecular_weight=round(self._analyzer.molecular_weight(), 2),
            aromaticity=round(self._analyzer.aromaticity(), 4),
            instability_index=round(self._analyzer.instability_index(), 2),
            isoelectric_point=round(self._analyzer.isoelectric_point(), 2),
            gravy=round(self._analyzer.gravy(), 4),
            helix_fraction=ss_fractions["helix_fraction"],
            turn_fraction=ss_fractions["turn_fraction"],
            sheet_fraction=ss_fractions["sheet_fraction"],
            amino_acid_composition=self.amino_acid_composition(),
        )

    def stability_classification(self) -> str:
        """Classify predicted stability using the standard instability-index cutoff."""
        instability = self._analyzer.instability_index()
        return "stable" if instability < 40.0 else "potentially unstable"

    def hydrophobicity_classification(self) -> str:
        """Classify overall hydrophobicity based on GRAVY sign."""
        return "hydrophobic" if self._analyzer.gravy() > 0 else "hydrophilic"

    @staticmethod
    def run() -> None:
        """Demonstrate physicochemical property computation for two proteins."""
        p53_fragment = ProteinAnalysisWorkflow(
            sequence="MEEPQSDPSVEPPLSQETFSDLWKLLPENNVLSPLPSQAMDDLMLSPDDIEQWFTEDPG",
            identifier="NP_000537.3_fragment",
        )
        report = p53_fragment.generate_report()
        print("Protein report:", report)
        print("Stability classification:", p53_fragment.stability_classification())
        print("Hydrophobicity classification:", p53_fragment.hydrophobicity_classification())

        insulin_b_chain = ProteinAnalysisWorkflow(
            sequence="FVNQHLCGSHLVEALYLVCGERGFFYTPKT",
            identifier="P01308_insulin_B_chain",
        )
        insulin_report = insulin_b_chain.generate_report()
        print("\nInsulin B-chain report:", insulin_report)
        print("Stability classification:", insulin_b_chain.stability_classification())
        print("Hydrophobicity classification:", insulin_b_chain.hydrophobicity_classification())


if __name__ == "__main__":
    ProteinAnalysisWorkflow.run()
