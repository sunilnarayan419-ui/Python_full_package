-- 1NF: atomic columns (already true above -- no repeating groups or arrays of values).

-- 2NF: every non-key attribute depends on the WHOLE primary key. In the denormalized
-- table above, compound/researcher/target attributes depend only on part of an implied
-- composite identity, not on screening_result_id as a whole -- split them out.

-- 3NF: eliminate transitive dependencies (e.g. researcher_email depends on researcher_name,
-- not directly on the result) by extracting Researcher and MolecularTarget as their own
-- entities with a single-column identity.

CREATE TABLE researchers (
    researcher_id     BIGSERIAL PRIMARY KEY,
    full_name            TEXT NOT NULL,
    email                   TEXT NOT NULL UNIQUE
);

CREATE TABLE molecular_targets (
    target_id            BIGSERIAL PRIMARY KEY,
    gene_symbol              TEXT NOT NULL,
    uniprot_accession           TEXT NOT NULL UNIQUE
);

CREATE TABLE compounds (
    compound_id             BIGSERIAL PRIMARY KEY,
    smiles                     TEXT NOT NULL,
    molecular_weight              NUMERIC(10,4) NOT NULL
);

CREATE TABLE screening_runs (
    screening_run_id           BIGSERIAL PRIMARY KEY,
    target_id                     BIGINT NOT NULL REFERENCES molecular_targets(target_id),
    operator_id                      BIGINT NOT NULL REFERENCES researchers(researcher_id),
    run_date                            DATE NOT NULL
);

CREATE TABLE screening_results (
    screening_result_id           BIGSERIAL PRIMARY KEY,
    screening_run_id                 BIGINT NOT NULL REFERENCES screening_runs(screening_run_id),
    compound_id                         BIGINT NOT NULL REFERENCES compounds(compound_id),
    potency_nm                             NUMERIC(12,4),
    UNIQUE (screening_run_id, compound_id)
);
-- Now: updating a researcher's email touches exactly one row. A researcher or target can
-- exist with zero screening results. Deleting a result never deletes target/researcher data.
