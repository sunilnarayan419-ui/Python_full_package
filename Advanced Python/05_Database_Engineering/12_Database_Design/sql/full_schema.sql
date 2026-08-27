-- Production schema: Drug Discovery Platform
-- ResearchProject -> Experiment -> Assay -> ScreeningRun -> ScreeningResult -> Compound

CREATE TABLE researchers (
    researcher_id       BIGSERIAL PRIMARY KEY,
    full_name           TEXT NOT NULL,
    email               TEXT NOT NULL UNIQUE,
    is_active            BOOLEAN NOT NULL DEFAULT TRUE,
    created_at            TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE research_projects (
    project_id            BIGSERIAL PRIMARY KEY,
    project_code            TEXT NOT NULL UNIQUE,
    title                     TEXT NOT NULL,
    owner_researcher_id       BIGINT NOT NULL REFERENCES researchers(researcher_id),
    status                     TEXT NOT NULL CHECK (status IN ('planning','active','on_hold','completed','cancelled')),
    started_at                 DATE NOT NULL,
    ended_at                   DATE,
    deleted_at                 TIMESTAMPTZ,          -- soft delete
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at                   TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_project_dates CHECK (ended_at IS NULL OR ended_at >= started_at)
);

CREATE TABLE experiments (
    experiment_id            BIGSERIAL PRIMARY KEY,
    project_id                 BIGINT NOT NULL REFERENCES research_projects(project_id),
    lead_researcher_id           BIGINT NOT NULL REFERENCES researchers(researcher_id),
    title                          TEXT NOT NULL,
    hypothesis                       TEXT NOT NULL,
    started_at                        DATE NOT NULL,
    created_at                          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_experiments_project_id ON experiments(project_id);

CREATE TABLE molecular_targets (
    target_id        BIGSERIAL PRIMARY KEY,
    gene_symbol         TEXT NOT NULL,
    uniprot_accession      TEXT NOT NULL UNIQUE,
    target_class             TEXT NOT NULL
);

CREATE TABLE assays (
    assay_id          BIGSERIAL PRIMARY KEY,
    experiment_id        BIGINT NOT NULL REFERENCES experiments(experiment_id),
    target_id              BIGINT NOT NULL REFERENCES molecular_targets(target_id),
    assay_name                TEXT NOT NULL,
    assay_type                  TEXT NOT NULL CHECK (assay_type IN ('binding','functional','adme','toxicity')),
    readout_unit                  TEXT NOT NULL
);

CREATE INDEX idx_assays_experiment_id ON assays(experiment_id);

CREATE TABLE compounds (
    compound_id             BIGSERIAL PRIMARY KEY,
    project_id                 BIGINT NOT NULL REFERENCES research_projects(project_id),
    parent_compound_id            BIGINT REFERENCES compounds(compound_id),
    inchi_key                        TEXT NOT NULL UNIQUE,
    smiles                              TEXT NOT NULL,
    molecular_weight                      NUMERIC(10,4) NOT NULL CHECK (molecular_weight > 0),
    synthesized_at                          DATE NOT NULL,
    created_at                                TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_compounds_project_id ON compounds(project_id);

CREATE TABLE screening_runs (
    screening_run_id       BIGSERIAL PRIMARY KEY,
    assay_id                  BIGINT NOT NULL REFERENCES assays(assay_id),
    operator_id                  BIGINT NOT NULL REFERENCES researchers(researcher_id),
    run_date                        DATE NOT NULL,
    plate_count                        INTEGER NOT NULL CHECK (plate_count > 0),
    created_at                            TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_screening_runs_assay_id ON screening_runs(assay_id);

CREATE TABLE screening_results (
    screening_result_id       BIGSERIAL PRIMARY KEY,
    screening_run_id             BIGINT NOT NULL REFERENCES screening_runs(screening_run_id) ON DELETE CASCADE,
    compound_id                     BIGINT NOT NULL REFERENCES compounds(compound_id),
    potency_nm                         NUMERIC(12,4) CHECK (potency_nm >= 0),
    is_hit                                 BOOLEAN NOT NULL DEFAULT FALSE,
    measured_at                               TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (screening_run_id, compound_id)
);

CREATE INDEX idx_screening_results_compound_id ON screening_results(compound_id);

-- Multi-tenant boundary: every top-level query for project-scoped data must filter by
-- organization_id, enforced at the application layer via the repository's mandatory
-- project_id parameter -- there is intentionally no unscoped "list all compounds" query.
CREATE TABLE organizations (
    organization_id       BIGSERIAL PRIMARY KEY,
    name                      TEXT NOT NULL UNIQUE
);

ALTER TABLE research_projects
    ADD COLUMN organization_id BIGINT NOT NULL REFERENCES organizations(organization_id);
CREATE INDEX idx_projects_organization_id ON research_projects(organization_id);
