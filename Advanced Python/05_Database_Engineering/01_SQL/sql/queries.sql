-- ============================================================
-- 1. Best potency per compound per target, ranked (window function)
-- ============================================================
SELECT
    c.compound_id,
    c.inchi_key,
    mt.gene_symbol,
    sr.potency_nm,
    RANK() OVER (
        PARTITION BY mt.target_id
        ORDER BY sr.potency_nm ASC NULLS LAST
    ) AS potency_rank
FROM screening_results sr
JOIN compounds c        ON c.compound_id = sr.compound_id
JOIN screening_runs run ON run.screening_run_id = sr.screening_run_id
JOIN assays a            ON a.assay_id = run.assay_id
JOIN molecular_targets mt ON mt.target_id = a.target_id
WHERE sr.potency_nm IS NOT NULL;


-- ============================================================
-- 2. Hit rate per assay with FILTER-based conditional aggregation
-- ============================================================
SELECT
    a.assay_id,
    a.assay_name,
    COUNT(*)                                            AS total_results,
    COUNT(*) FILTER (WHERE sr.is_hit)                   AS total_hits,
    ROUND(
        COUNT(*) FILTER (WHERE sr.is_hit)::NUMERIC
        / NULLIF(COUNT(*), 0) * 100,
        2
    )                                                    AS hit_rate_pct
FROM screening_results sr
JOIN screening_runs run ON run.screening_run_id = sr.screening_run_id
JOIN assays a ON a.assay_id = run.assay_id
GROUP BY a.assay_id, a.assay_name
HAVING COUNT(*) >= 10
ORDER BY hit_rate_pct DESC;


-- ============================================================
-- 3. Recursive CTE: full derivative lineage of a compound
-- ============================================================
WITH RECURSIVE compound_lineage AS (
    SELECT
        compound_id,
        parent_compound_id,
        inchi_key,
        0 AS depth
    FROM compounds
    WHERE compound_id = $1

    UNION ALL

    SELECT
        c.compound_id,
        c.parent_compound_id,
        c.inchi_key,
        cl.depth + 1
    FROM compounds c
    JOIN compound_lineage cl ON c.parent_compound_id = cl.compound_id
)
SELECT * FROM compound_lineage
ORDER BY depth;


-- ============================================================
-- 4. Projects with active screening in the last 30 days (EXISTS)
-- ============================================================
SELECT
    rp.project_id,
    rp.project_code,
    rp.title
FROM research_projects rp
WHERE EXISTS (
    SELECT 1
    FROM compounds c
    JOIN screening_results sr ON sr.compound_id = c.compound_id
    JOIN screening_runs run ON run.screening_run_id = sr.screening_run_id
    WHERE c.project_id = rp.project_id
      AND run.run_date >= (CURRENT_DATE - INTERVAL '30 days')
)
ORDER BY rp.project_code;


-- ============================================================
-- 5. Per-project compound potency distribution (CTE + aggregation)
-- ============================================================
WITH project_potencies AS (
    SELECT
        c.project_id,
        sr.potency_nm,
        CASE
            WHEN sr.potency_nm < 100  THEN 'sub_100nm'
            WHEN sr.potency_nm < 1000 THEN 'sub_1um'
            ELSE 'weak'
        END AS potency_band
    FROM compounds c
    JOIN screening_results sr ON sr.compound_id = c.compound_id
    WHERE sr.potency_nm IS NOT NULL
)
SELECT
    rp.project_code,
    pp.potency_band,
    COUNT(*)              AS compound_count,
    ROUND(AVG(pp.potency_nm), 2) AS avg_potency_nm
FROM project_potencies pp
JOIN research_projects rp ON rp.project_id = pp.project_id
GROUP BY rp.project_code, pp.potency_band
ORDER BY rp.project_code, pp.potency_band;


-- ============================================================
-- 6. Compounds never screened (anti-join via NOT EXISTS)
-- ============================================================
SELECT c.compound_id, c.inchi_key, c.synthesized_at
FROM compounds c
WHERE NOT EXISTS (
    SELECT 1 FROM screening_results sr WHERE sr.compound_id = c.compound_id
)
ORDER BY c.synthesized_at DESC;


-- ============================================================
-- 7. Rolling 7-run moving average of hit rate per assay (window frame)
-- ============================================================
WITH run_hit_rates AS (
    SELECT
        run.screening_run_id,
        run.assay_id,
        run.run_date,
        COUNT(*) FILTER (WHERE sr.is_hit)::NUMERIC / NULLIF(COUNT(*), 0) AS hit_rate
    FROM screening_runs run
    JOIN screening_results sr ON sr.screening_run_id = run.screening_run_id
    GROUP BY run.screening_run_id, run.assay_id, run.run_date
)
SELECT
    assay_id,
    run_date,
    hit_rate,
    ROUND(
        AVG(hit_rate) OVER (
            PARTITION BY assay_id
            ORDER BY run_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ),
        4
    ) AS rolling_7run_avg_hit_rate
FROM run_hit_rates
ORDER BY assay_id, run_date;


-- ============================================================
-- 8. Parameterized UPSERT with conflict handling
-- ============================================================
INSERT INTO screening_results (
    screening_run_id, compound_id, potency_nm, percent_inhibition, is_hit
)
VALUES ($1, $2, $3, $4, $5)
ON CONFLICT (screening_run_id, compound_id)
DO UPDATE SET
    potency_nm         = EXCLUDED.potency_nm,
    percent_inhibition  = EXCLUDED.percent_inhibition,
    is_hit               = EXCLUDED.is_hit,
    measured_at            = now()
RETURNING screening_result_id;


-- ============================================================
-- 9. Soft-scoped update within a transaction boundary
-- ============================================================
UPDATE research_projects
SET status = 'completed',
    ended_at = $2
WHERE project_id = $1
  AND status = 'active'
RETURNING project_id, status, ended_at;


-- ============================================================
-- 10. Bulk delete of orphaned screening runs (bounded, explicit)
-- ============================================================
DELETE FROM screening_runs
WHERE screening_run_id IN (
    SELECT run.screening_run_id
    FROM screening_runs run
    LEFT JOIN screening_results sr ON sr.screening_run_id = run.screening_run_id
    WHERE sr.screening_result_id IS NULL
      AND run.run_date < (CURRENT_DATE - INTERVAL '365 days')
    LIMIT 500
)
RETURNING screening_run_id;
