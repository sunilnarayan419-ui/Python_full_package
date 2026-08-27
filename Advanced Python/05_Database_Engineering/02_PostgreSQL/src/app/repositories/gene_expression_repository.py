from __future__ import annotations

import json
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from app.database.connection import acquire_connection


@dataclass(frozen=True, slots=True)
class GeneAnnotationMatch:
    gene_id: UUID
    symbol: str
    annotations: dict


class GeneExpressionRepository:
    async def find_genes_by_pathway(self, pathway: str) -> list[GeneAnnotationMatch]:
        query = """
            SELECT gene_id, symbol, annotations
            FROM genes
            WHERE annotations @> $1::jsonb
        """
        async with acquire_connection() as conn:
            rows = await conn.fetch(query, json.dumps({"pathway": pathway}))
        return [
            GeneAnnotationMatch(
                gene_id=row["gene_id"],
                symbol=row["symbol"],
                annotations=json.loads(row["annotations"]),
            )
            for row in rows
        ]

    async def search_gene_descriptions(self, terms: str) -> list[GeneAnnotationMatch]:
        query = """
            SELECT gene_id, symbol, annotations
            FROM genes
            WHERE annotation_search @@ plainto_tsquery('english', $1)
            LIMIT 100
        """
        async with acquire_connection() as conn:
            rows = await conn.fetch(query, terms)
        return [
            GeneAnnotationMatch(
                gene_id=row["gene_id"],
                symbol=row["symbol"],
                annotations=json.loads(row["annotations"]),
            )
            for row in rows
        ]

    async def claim_sequenced_samples(self, batch_size: int = 10) -> list[UUID]:
        """Uses FOR UPDATE SKIP LOCKED so concurrent workers never claim the same row."""
        async with acquire_connection() as conn:
            async with conn.transaction():
                rows = await conn.fetch(
                    """
                    SELECT sample_id FROM samples
                    WHERE status = 'sequenced'
                    ORDER BY created_at
                    LIMIT $1
                    FOR UPDATE SKIP LOCKED
                    """,
                    batch_size,
                )
                sample_ids = [row["sample_id"] for row in rows]
                if sample_ids:
                    await conn.execute(
                        "UPDATE samples SET status = 'analyzed' WHERE sample_id = ANY($1::uuid[])",
                        sample_ids,
                    )
        return sample_ids

    async def record_expression(
        self, *, sample_id: UUID, gene_id: UUID, read_count: int, tpm: Decimal
    ) -> None:
        query = """
            INSERT INTO gene_expression_reads (sample_id, gene_id, read_count, tpm)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (sample_id, gene_id)
            DO UPDATE SET read_count = EXCLUDED.read_count, tpm = EXCLUDED.tpm
        """
        async with acquire_connection() as conn:
            await conn.execute(query, sample_id, gene_id, read_count, tpm)
