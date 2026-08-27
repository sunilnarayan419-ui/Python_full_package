from __future__ import annotations

from dataclasses import dataclass
from io import StringIO

from Bio.PDB import PDBParser
from Bio.PDB.Structure import Structure

# Minimal, well-formed embedded PDB record fragment (mock coordinates,
# realistic record types) representing a short polypeptide chain.
_MOCK_PDB_TEXT = """\
HEADER    HYDROLASE                              01-JAN-24   MOCK
TITLE     MOCK STRUCTURE FOR STRUCTURAL-BIOLOGY WORKFLOW DEMONSTRATION
ATOM      1  N   MET A   1      11.104  13.207   2.140  1.00 20.00           N
ATOM      2  CA  MET A   1      12.560  13.298   2.211  1.00 20.00           C
ATOM      3  C   MET A   1      13.045  14.673   1.762  1.00 20.00           C
ATOM      4  O   MET A   1      12.328  15.451   1.130  1.00 20.00           O
ATOM      5  N   GLU A   2      14.310  14.965   2.101  1.00 19.50           N
ATOM      6  CA  GLU A   2      14.923  16.256   1.789  1.00 19.50           C
ATOM      7  C   GLU A   2      16.401  16.213   2.145  1.00 19.50           C
ATOM      8  O   GLU A   2      16.847  15.401   2.957  1.00 19.50           O
ATOM      9  N   GLU A   3      17.156  17.106   1.512  1.00 21.00           N
ATOM     10  CA  GLU A   3      18.598  17.185   1.741  1.00 21.00           C
ATOM     11  C   GLU A   3      19.201  18.489   1.219  1.00 21.00           C
ATOM     12  O   GLU A   3      18.564  19.246   0.481  1.00 21.00           O
HETATM   13  O   HOH A 101      20.500  19.800   0.900  1.00 30.00           O
TER      14      GLU A   3
ATOM     15  N   PRO B   1      25.104  13.207   2.140  1.00 22.00           N
ATOM     16  CA  PRO B   1      26.560  13.298   2.211  1.00 22.00           C
ATOM     17  C   PRO B   1      27.045  14.673   1.762  1.00 22.00           C
ATOM     18  O   PRO B   1      26.328  15.451   1.130  1.00 22.00           O
TER      19      PRO B   1
END
"""


@dataclass
class ChainSummary:
    """Summary statistics for a single structural chain."""

    chain_id: str
    residue_count: int
    het_residue_count: int
    atom_count: int


class ProteinStructureWorkflow:
    """Industry-level structural-biology workflow built on Bio.PDB.

    Parses PDB-format coordinate data and provides hierarchy-aware
    summaries (Structure -> Model -> Chain -> Residue -> Atom) commonly
    required in structure-based drug-discovery pipelines.
    """

    def __init__(self, pdb_text: str, structure_id: str) -> None:
        """Initialize by parsing embedded or externally supplied PDB text.

        Args:
            pdb_text: Raw PDB-format structure content.
            structure_id: Local label for the parsed structure (not
                asserted to be a live RCSB record).
        """
        if not self.validate_pdb_text(pdb_text):
            raise ValueError("Input does not contain any parsable ATOM/HETATM records")

        parser = PDBParser(QUIET=True)
        self.structure_id = structure_id
        self.structure: Structure = parser.get_structure(structure_id, StringIO(pdb_text))

    @staticmethod
    def validate_pdb_text(pdb_text: str) -> bool:
        """Validate that the supplied text contains coordinate records."""
        if not pdb_text or not pdb_text.strip():
            return False
        return any(line.startswith(("ATOM", "HETATM")) for line in pdb_text.splitlines())

    def list_chains(self) -> list[str]:
        """Return chain identifiers present in the first model of the structure."""
        model = self.structure[0]
        return [chain.id for chain in model]

    def chain_summary(self, chain_id: str) -> ChainSummary:
        """Compute residue and atom counts for a specific chain.

        Args:
            chain_id: Identifier of the chain to summarize (e.g. "A").
        """
        model = self.structure[0]
        if chain_id not in {c.id for c in model}:
            raise KeyError(f"Chain {chain_id!r} not found in structure")

        chain = model[chain_id]
        residue_count = 0
        het_residue_count = 0
        atom_count = 0
        for residue in chain:
            hetero_flag = residue.id[0]
            if hetero_flag.strip():
                het_residue_count += 1
            else:
                residue_count += 1
            atom_count += len(list(residue.get_atoms()))

        return ChainSummary(
            chain_id=chain_id,
            residue_count=residue_count,
            het_residue_count=het_residue_count,
            atom_count=atom_count,
        )

    def structure_summary(self) -> dict[str, int]:
        """Compute an overall summary across every chain in the first model."""
        model = self.structure[0]
        total_residues = 0
        total_atoms = 0
        for chain in model:
            for residue in chain:
                total_residues += 1
                total_atoms += len(list(residue.get_atoms()))
        return {
            "chain_count": len(list(model)),
            "residue_count": total_residues,
            "atom_count": total_atoms,
        }

    def get_ca_coordinates(self, chain_id: str) -> list[tuple[float, float, float]]:
        """Extract alpha-carbon coordinates for a chain, used for backbone tracing.

        Args:
            chain_id: Identifier of the chain whose CA atoms should be extracted.
        """
        model = self.structure[0]
        chain = model[chain_id]
        coordinates: list[tuple[float, float, float]] = []
        for residue in chain:
            if "CA" in residue:
                x, y, z = residue["CA"].get_coord()
                coordinates.append((float(x), float(y), float(z)))
        return coordinates

    @staticmethod
    def run() -> None:
        """Demonstrate structure parsing and hierarchy-aware summarization."""
        workflow = ProteinStructureWorkflow(_MOCK_PDB_TEXT, structure_id="MOCK_STRUCT")

        chains = workflow.list_chains()
        print(f"Chains detected: {chains}")

        for chain_id in chains:
            summary = workflow.chain_summary(chain_id)
            print(f"  Chain {summary.chain_id}: "
                  f"{summary.residue_count} residues, "
                  f"{summary.het_residue_count} het-groups, "
                  f"{summary.atom_count} atoms")

        print("Overall structure summary:", workflow.structure_summary())

        ca_coords = workflow.get_ca_coordinates("A")
        print(f"Chain A alpha-carbon trace ({len(ca_coords)} residues):")
        for coord in ca_coords:
            print(f"  {coord}")


if __name__ == "__main__":
    ProteinStructureWorkflow.run()
