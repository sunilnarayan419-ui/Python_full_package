CREATE TABLE compounds (
    compound_id     BIGSERIAL PRIMARY KEY,
    project_id      BIGINT NOT NULL,
    inchi_key       TEXT NOT NULL UNIQUE,
    smiles          TEXT NOT NULL,
    molecular_weight NUMERIC(10,4) NOT NULL,
    is_archived     BOOLEAN NOT NULL DEFAULT FALSE,
    tags            TEXT[] NOT NULL DEFAULT '{}',
    metadata        JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
