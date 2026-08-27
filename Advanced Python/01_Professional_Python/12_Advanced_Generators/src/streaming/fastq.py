"""Streaming FASTQ parsing.

FASTQ files for whole-genome sequencing runs are routinely tens of
gigabytes; materializing them into a `list[FastqRecord]` is not
viable. This module reads and yields one record at a time, so peak
memory stays O(1) with respect to file size.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import IO, Iterator


@dataclass(frozen=True, slots=True)
class FastqRecord:
    identifier: str
    sequence: str
    quality: str


def iter_fastq_records(stream: IO[str]) -> Iterator[FastqRecord]:
    while True:
        header = stream.readline()
        if not header:
            return
        sequence = stream.readline().rstrip("\n")
        plus_line = stream.readline()
        quality = stream.readline().rstrip("\n")
        if not plus_line or not quality:
            raise ValueError("truncated FASTQ record encountered")
        yield FastqRecord(identifier=header.rstrip("\n").lstrip("@"), sequence=sequence, quality=quality)
