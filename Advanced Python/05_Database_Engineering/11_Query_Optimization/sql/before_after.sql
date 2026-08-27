-- ============================================================
-- BEFORE: N+1 via application-level loop (documented, not executed here --
-- see repositories/experiment_repository.py for the Python before/after pair)
-- ============================================================

-- ============================================================
-- BEFORE: unbounded scan pulling every column for a listing page
-- ============================================================
EXPLAIN ANALYZE
SELECT * FROM screening_results
WHERE compound_id IN (SELECT compound_id FROM compounds WHERE project_id = 42);

-- AFTER: project only needed columns, push filtering into a join, add LIMIT/OFFSET
-- keyset pagination instead of OFFSET for deep pages.
EXPLAIN ANALYZE
SELECT sr.screening_result_id, sr.compound_id, sr.potency_nm
FROM screening_results sr
JOIN compounds c ON c.compound_id = sr.compound_id
WHERE c.project_id = 42
  AND sr.screening_result_id > $1   -- keyset cursor instead of OFFSET
ORDER BY sr.screening_result_id
LIMIT 50;

-- ============================================================
-- BEFORE: correlated subquery re-executed per outer row
-- ============================================================
EXPLAIN ANALYZE
SELECT
    c.compound_id,
    (SELECT COUNT(*) FROM screening_results sr WHERE sr.compound_id = c.compound_id) AS result_count
FROM compounds c
WHERE c.project_id = 42;

-- AFTER: single aggregation join, computed once per group
EXPLAIN ANALYZE
SELECT c.compound_id, COUNT(sr.screening_result_id) AS result_count
FROM compounds c
LEFT JOIN screening_results sr ON sr.compound_id = c.compound_id
WHERE c.project_id = 42
GROUP BY c.compound_id;

-- ============================================================
-- BEFORE: repeated full aggregation on every dashboard read
-- ============================================================
EXPLAIN ANALYZE
SELECT a.assay_id, COUNT(*) FILTER (WHERE sr.is_hit) AS hits
FROM screening_results sr
JOIN screening_runs run ON run.screening_run_id = sr.screening_run_id
JOIN assays a ON a.assay_id = run.assay_id
GROUP BY a.assay_id;

-- AFTER: precomputed materialized view refreshed on a schedule, dashboard reads become
-- a plain index scan against a small summary table (see 14_Views for the definition).
EXPLAIN ANALYZE
SELECT assay_id, hits FROM mv_assay_hit_counts WHERE assay_id = 7;
