"""Demonstrates the re module for validating and extracting scientific identifiers."""

import re


class UniversityRe:
    """Introduces basic pattern matching using sample ID validation."""

    SAMPLE_ID_PATTERN = re.compile(r"^PL-\d{3,5}$")

    def is_valid_sample_id(self, sample_id: str) -> bool:
        return bool(self.SAMPLE_ID_PATTERN.match(sample_id))

    @staticmethod
    def run() -> None:
        demo = UniversityRe()
        for sample_id in ["PL-042", "PL-1", "sample_042"]:
            print(f"'{sample_id}' is a valid sample ID: {demo.is_valid_sample_id(sample_id)}")


class InterviewRe:
    """Solves a gene-identifier extraction problem, handling malformed input."""

    GENE_ID_PATTERN = re.compile(r"\b([A-Z0-9]{2,10})_(\d{3,6})\b")

    def extract_gene_identifiers(self, text: str) -> list[tuple[str, str]]:
        """Extract (gene_symbol, numeric_id) pairs from free-form text.

        Returns an empty list rather than raising when no matches are found,
        since text legitimately containing zero gene identifiers is expected.
        """
        return self.GENE_ID_PATTERN.findall(text)

    def validate_dna_sequence(self, sequence: str) -> bool:
        """Validate that a string contains only standard DNA bases."""
        if not sequence:
            return False
        return bool(re.fullmatch(r"[ACGT]+", sequence))

    @staticmethod
    def run() -> None:
        solver = InterviewRe()

        # Test case 1: text containing valid gene identifiers
        text = "Notes: BRCA1_001 was upregulated; see also TP53_00042 for context."
        identifiers = solver.extract_gene_identifiers(text)
        print(f"Extracted gene identifiers: {identifiers}")

        # Test case 2: edge case, no matches
        print(f"Extracted from unrelated text: {solver.extract_gene_identifiers('no ids here')}")

        # Test case 3: DNA sequence validation, valid and invalid cases
        print(f"'ACGTACGT' is valid DNA: {solver.validate_dna_sequence('ACGTACGT')}")
        print(f"'ACGTXYZT' is valid DNA: {solver.validate_dna_sequence('ACGTXYZT')}")
        print(f"'' is valid DNA: {solver.validate_dna_sequence('')}")


class IndustryRe:
    """Reusable scientific metadata parser built on precompiled regex patterns.

    Regular expressions are used here only for validating and extracting simple,
    well-defined tokens (IDs, motifs). Parsing complex structured formats (e.g.
    full FASTA or GFF files) should use a dedicated parser instead.
    """

    LAB_ID_PATTERN = re.compile(r"^(?P<lab>[A-Z]{2,4})-(?P<year>\d{4})-(?P<sequence>\d{3,5})$")
    WHITESPACE_PATTERN = re.compile(r"\s+")

    def parse_lab_identifier(self, identifier: str) -> dict[str, str]:
        """Parse a structured laboratory identifier like 'GEN-2026-00042'.

        Raises ValueError for an identifier that does not match the expected
        structure, since silently returning partial data could mislead a
        downstream reporting pipeline.
        """
        match = self.LAB_ID_PATTERN.fullmatch(identifier)
        if match is None:
            raise ValueError(f"Identifier does not match expected format: '{identifier}'")
        return match.groupdict()

    def clean_metadata_text(self, raw_text: str) -> str:
        """Collapse irregular whitespace in free-form metadata text."""
        return self.WHITESPACE_PATTERN.sub(" ", raw_text).strip()

    def find_motif_positions(self, sequence: str, motif: str) -> list[int]:
        """Find all zero-based start positions of a DNA motif within a sequence."""
        if not re.fullmatch(r"[ACGT]*", sequence):
            raise ValueError("sequence must contain only A, C, G, T bases.")
        if not re.fullmatch(r"[ACGT]+", motif):
            raise ValueError("motif must contain only A, C, G, T bases.")

        return [match.start() for match in re.finditer(f"(?={re.escape(motif)})", sequence)]

    @staticmethod
    def run() -> None:
        parser = IndustryRe()

        parsed = parser.parse_lab_identifier("GEN-2026-00042")
        print(f"Parsed lab identifier: {parsed}")

        try:
            parser.parse_lab_identifier("invalid-id")
        except ValueError as error:
            print(f"Handled invalid identifier: {error}")

        cleaned = parser.clean_metadata_text("species:   Zea mays \n\t height: 88cm")
        print(f"Cleaned metadata text: '{cleaned}'")

        positions = parser.find_motif_positions("ACGTACGTACGT", "GTA")
        print(f"Motif 'GTA' found at positions: {positions}")


if __name__ == "__main__":
    UniversityRe.run()
    InterviewRe.run()
    IndustryRe.run()
