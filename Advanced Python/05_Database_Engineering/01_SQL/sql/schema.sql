-- Drug Discovery Platform - Core Schema
-- PostgreSQL 15+

CREATE TABLE researchers (
    researcher_id       BIGSERIAL PRIMARY KEY,
    full_name           TEXT NOT NULL,
    email               TEXT NOT NULL UNIQUE,
    department          TEXT NOT NULL,
    is_active           BOOLEAN NOT NULL DEFAULT TRUE,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE research_projects (
    project_id          BIGSERIAL PRIMARY KEY,
    project_code        TEXT NOT NULL UNIQUE,
    title               TEXT NOT NULL,
    lead_researcher_id  BIGINT NOT NULL REFERENCES researchers(researcher_id),
    status              TEXT NOT NULL CHECK (status IN ('planning','active','on_hold','completed','cancelled')),
    started_at          DATE NOT NULL,
    ended_at            DATE,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_project_dates CHECK (ended_at IS NULL OR ended_at >= started_at)
);

CREATE TABLE molecular_targets (
    target_id           BIGSERIAL PRIMARY KEY,
    gene_symbol         TEXT NOT NULL,
    uniprot_accession   TEXT NOT NULL UNIQUE,
    target_class        TEXT NOT NULL,
    organism             TEXT NOT NULL DEFAULT 'Homo sapiens',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE compounds (
    compound_id          BIGSERIAL PRIMARY KEY,
    project_id           BIGINT NOT NULL REFERENCES research_projects(project_id),
    parent_compound_id   BIGINT REFERENCES compounds(compound_id),
    smiles                TEXT NOT NULL,
    molecular_weight      NUMERIC(10,4) NOT NULL CHECK (molecular_weight > 0),
    inchi_key             TEXT NOT NULL UNIQUE,
    synthesized_at         DATE NOT NULL,
    created_at             TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_compounds_project_id ON compounds(project_id);
CREATE INDEX idx_compounds_parent_id ON compounds(parent_compound_id);

CREATE TABLE assays (
    assay_id             BIGSERIAL PRIMARY KEY,
    target_id             BIGINT NOT NULL REFERENCES molecular_targets(target_id),
    assay_name             TEXT NOT NULL,
    assay_type              TEXT NOT NULL CHECK (assay_type IN ('binding','functional','adme','toxicity')),
    readout_unit             TEXT NOT NULL,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE screening_runs (
    screening_run_id       BIGSERIAL PRIMARY KEY,
    assay_id                BIGINT NOT NULL REFERENCES assays(assay_id),
    operator_id              BIGINT NOT NULL REFERENCES researchers(researcher_id),
    run_date                  DATE NOT NULL,
    plate_count                INTEGER NOT NULL CHECK (plate_count > 0),
    created_at                TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_screening_runs_assay_id ON screening_runs(assay_id);

CREATE TABLE screening_results (
    screening_result_id      BIGSERIAL PRIMARY KEY,
    screening_run_id           BIGINT NOT NULL REFERENCES screening_runs(screening_run_id) ON DELETE CASCADE,
    compound_id                  BIGINT NOT NULL REFERENCES compounds(compound_id),
    potency_nm                    NUMERIC(12,4) CHECK (potency_nm >= 0),
    percent_inhibition             NUMERIC(5,2) CHECK (percent_inhibition BETWEEN -20 AND 120),
    is_hit                          BOOLEAN NOT NULL DEFAULT FALSE,
    measured_at                     TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (screening_run_id, compound_id)
);

CREATE INDEX idx_screening_results_compound_id ON screening_results(compound_id);
CREATE INDEX idx_screening_results_run_id ON screening_results(screening_run_id);
CREATE INDEX idx_screening_results_hits ON screening_results(compound_id) WHERE is_hit = TRUE;
