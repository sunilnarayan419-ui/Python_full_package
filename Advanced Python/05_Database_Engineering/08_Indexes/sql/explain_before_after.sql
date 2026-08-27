-- BEFORE: no supporting index -> sequential scan over the whole table
EXPLAIN (ANALYZE, BUFFERS)
SELECT compound_id, inchi_key
FROM compounds
WHERE project_id = 42 AND is_archived = FALSE
ORDER BY created_at DESC
LIMIT 20;

-- Run after creating idx_compounds_active and idx_compounds_project_created:
-- the planner should switch to an Index Scan / Bitmap Index Scan and drop the Sort node
-- when created_at DESC matches the index's declared order.
EXPLAIN (ANALYZE, BUFFERS)
SELECT compound_id, inchi_key
FROM compounds
WHERE project_id = 42 AND is_archived = FALSE
ORDER BY created_at DESC
LIMIT 20;

-- Index-only scan check: with idx_compounds_project_covering, Postgres should report
-- "Index Only Scan" and a low/zero "Heap Fetches" count in EXPLAIN (ANALYZE, BUFFERS).
EXPLAIN (ANALYZE, BUFFERS)
SELECT project_id, molecular_weight, inchi_key
FROM compounds
WHERE project_id = 42;

-- Tag containment using the GIN index
EXPLAIN ANALYZE
SELECT compound_id FROM compounds WHERE tags @> ARRAY['kinase_inhibitor'];
