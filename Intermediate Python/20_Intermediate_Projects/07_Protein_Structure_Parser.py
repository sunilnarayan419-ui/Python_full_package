from __future__ import annotations

import io
import logging
from dataclasses import dataclass

from Bio.PDB.PDBParser import PDBParser
from Bio.PDB.Structure import Structure

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")


class StructureParsingError(Exception):
    """Raised when PDB-format structure data cannot be parsed."""


@dataclass(frozen=True, slots=True)
class ChainStatistics:
    chain_id: str
    residue_count: int
    atom_count: int


@dataclass(frozen=True, slots=True)
class StructureStatistics:
    structure_id: str
    model_count: int
    chain_statistics: tuple[ChainStatistics, ...]
    total_atom_count: int
    total_residue_count: int
    ca_coordinates: tuple[tuple[float, float, float], ...]


class ProteinStructureParser:
    """Parses PDB-format structure data and computes basic structural statistics.

    Statistics produced here are purely descriptive (counts and coordinates)
    and carry no functional or clinical interpretation.
    """

    def __init__(self) -> None:
        self._parser = PDBParser(QUIET=True)

    def parse(self, structure_id: str, pdb_text: str) -> Structure:
        if not pdb_text.strip():
            raise StructureParsingError("PDB content is empty.")
        try:
            handle = io.StringIO(pdb_text)
            structure = self._parser.get_structure(structure_id, handle)
        except Exception as exc:  # Bio.PDB raises varied internal exceptions on malformed input
            raise StructureParsingError(f"Failed to parse structure '{structure_id}'.") from exc

        if len(structure) == 0:
            raise StructureParsingError(f"Structure '{structure_id}' contains no models.")
        return structure

    def compute_statistics(self, structure: Structure) -> StructureStatistics:
        chain_stats: list[ChainStatistics] = []
        total_atoms = 0
        total_residues = 0
        ca_coordinates: list[tuple[float, float, float]] = []

        first_model = next(iter(structure))
        for chain in first_model:
            residues = list(chain)
            atom_count = sum(1 for residue in residues for _ in residue)
            chain_stats.append(
                ChainStatistics(
                    chain_id=chain.id,
                    residue_count=len(residues),
                    atom_count=atom_count,
                )
            )
            total_residues += len(residues)
            total_atoms += atom_count

            for residue in residues:
                if "CA" in residue:
                    coord = residue["CA"].get_coord()
                    ca_coordinates.append((round(float(coord[0]), 3), round(float(coord[1]), 3), round(float(coord[2]), 3)))

        return StructureStatistics(
            structure_id=structure.id,
            model_count=len(structure),
            chain_statistics=tuple(chain_stats),
            total_atom_count=total_atoms,
            total_residue_count=total_residues,
            ca_coordinates=tuple(ca_coordinates),
        )


def _build_sample_pdb_text() -> str:
    """A minimal, controlled PDB-format record used for offline demonstration."""
    return """\
ATOM      1  N   ALA A   1      11.104  13.207   2.145  1.00 20.00           N
ATOM      2  CA  ALA A   1      12.560  13.207   2.145  1.00 20.00           C
ATOM      3  C   ALA A   1      13.100  14.610   2.145  1.00 20.00           C
ATOM      4  O   ALA A   1      12.400  15.610   2.200  1.00 20.00           O
ATOM      5  N   GLY A   2      14.430  14.650   2.100  1.00 20.00           N
ATOM      6  CA  GLY A   2      15.050  15.960   2.100  1.00 20.00           C
ATOM      7  C   GLY A   2      16.560  15.900   2.150  1.00 20.00           C
ATOM      8  O   GLY A   2      17.200  14.860   2.200  1.00 20.00           O
ATOM      9  N   SER B   1      20.100  10.200   5.000  1.00 20.00           N
ATOM     10  CA  SER B   1      21.500  10.200   5.000  1.00 20.00           C
ATOM     11  C   SER B   1      22.100  11.600   5.000  1.00 20.00           C
ATOM     12  O   SER B   1      21.400  12.600   5.050  1.00 20.00           O
TER
END
"""


def run() -> StructureStatistics:
    """Parses a controlled example structure and reports basic statistics."""
    parser = ProteinStructureParser()
    pdb_text = _build_sample_pdb_text()

    structure = parser.parse("EXAMPLE_1", pdb_text)
    statistics = parser.compute_statistics(structure)

    logger.info("Structure: %s (%d model(s))", statistics.structure_id, statistics.model_count)
    for chain_stat in statistics.chain_statistics:
        logger.info(
            "Chain %s: %d residues, %d atoms", chain_stat.chain_id, chain_stat.residue_count, chain_stat.atom_count
        )
    logger.info("Total residues: %d, total atoms: %d", statistics.total_residue_count, statistics.total_atom_count)
    logger.info("CA coordinates captured: %d", len(statistics.ca_coordinates))

    return statistics


if __name__ == "__main__":
    run()
