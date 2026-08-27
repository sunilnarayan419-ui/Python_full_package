-- 1. B-tree: standard equality/range lookups (default index type)
CREATE INDEX idx_compounds_project_id ON compounds (project_id);

-- 2. Composite index: supports queries filtering project_id AND ordering by created_at.
--    Column order matters -- project_id (equality) must lead created_at (range/order).
CREATE INDEX idx_compounds_project_created ON compounds (project_id, created_at DESC);

-- 3. Partial index: only index the 5% of rows that are actively queried (non-archived).
--    Smaller index, faster writes on archived rows, faster reads on the hot path.
CREATE INDEX idx_compounds_active ON compounds (project_id) WHERE is_archived = FALSE;

-- 4. Unique index: enforced uniqueness that also accelerates exact-match lookups.
--    (Already declared via UNIQUE in schema.sql; shown here for explicitness.)
-- CREATE UNIQUE INDEX uq_compounds_inchi_key ON compounds (inchi_key);

-- 5. Expression index: supports case-insensitive lookups without a functional scan.
CREATE INDEX idx_compounds_smiles_lower ON compounds (lower(smiles));

-- 6. GIN index on array column: supports "contains tag" queries.
CREATE INDEX idx_compounds_tags_gin ON compounds USING GIN (tags);

-- 7. GIN index on JSONB with jsonb_path_ops: smaller, faster for containment (@>) queries
--    specifically (does not support key-existence ? operator).
CREATE INDEX idx_compounds_metadata_gin ON compounds USING GIN (metadata jsonb_path_ops);

-- 8. Covering index (INCLUDE): satisfies index-only scans for a narrow reporting query
--    without visiting the heap for molecular_weight.
CREATE INDEX idx_compounds_project_covering
    ON compounds (project_id) INCLUDE (molecular_weight, inchi_key);
