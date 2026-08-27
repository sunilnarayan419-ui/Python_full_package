-- PostgreSQL-native feature schema: Bioinformatics Data Platform
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TYPE sample_status AS ENUM ('collected', 'sequencing', 'sequenced', 'analyzed', 'failed');

CREATE TABLE genes (
    gene_id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    symbol          TEXT NOT NULL,
    chromosome      TEXT NOT NULL,
    aliases         TEXT[] NOT NULL DEFAULT '{}',
    annotations     JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX uq_genes_symbol_chromosome ON genes (symbol, chromosome);
CREATE INDEX idx_genes_aliases_gin ON genes USING GIN (aliases);
CREATE INDEX idx_genes_annotations_gin ON genes USING GIN (annotations jsonb_path_ops);

CREATE TABLE samples (
    sample_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subject_code    TEXT NOT NULL,
    collected_at    TIMESTAMPTZ NOT NULL,
    status          sample_status NOT NULL DEFAULT 'collected',
    metadata        JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_samples_status ON samples (status);
CREATE INDEX idx_samples_active
    ON samples (subject_code)
    WHERE status IN ('collected', 'sequencing');

CREATE TABLE gene_expression_reads (
    read_id         BIGSERIAL PRIMARY KEY,
    sample_id       UUID NOT NULL REFERENCES samples(sample_id) ON DELETE CASCADE,
    gene_id         UUID NOT NULL REFERENCES genes(gene_id),
    read_count      BIGINT NOT NULL CHECK (read_count >= 0),
    tpm             NUMERIC(14,6) NOT NULL CHECK (tpm >= 0),
    recorded_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (sample_id, gene_id)
);

CREATE INDEX idx_expression_gene_id ON gene_expression_reads (gene_id);
CREATE INDEX idx_expression_high_tpm ON gene_expression_reads (gene_id, tpm) WHERE tpm > 100;

-- Full-text search over annotation free text
ALTER TABLE genes ADD COLUMN annotation_search tsvector
    GENERATED ALWAYS AS (to_tsvector('english', coalesce(annotations->>'description', ''))) STORED;
CREATE INDEX idx_genes_annotation_fts ON genes USING GIN (annotation_search);
