-- Standard view: simplifies a recurring 4-table join without duplicating business logic.
CREATE VIEW v_compound_screening_overview AS
SELECT
    c.compound_id,
    c.inchi_key,
    mt.gene_symbol,
    sr.potency_nm,
    sr.is_hit,
    run.run_date
FROM compounds c
JOIN screening_results sr ON sr.compound_id = c.compound_id
JOIN screening_runs run ON run.screening_run_id = sr.screening_run_id
JOIN assays a ON a.assay_id = run.assay_id
JOIN molecular_targets mt ON mt.target_id = a.target_id;

-- Reporting view: aggregated, read-only, used by dashboards -- never written to directly.
CREATE VIEW v_project_hit_summary AS
SELECT
    rp.project_id,
    rp.project_code,
    COUNT(sr.screening_result_id) AS total_results,
    COUNT(sr.screening_result_id) FILTER (WHERE sr.is_hit) AS total_hits
FROM research_projects rp
JOIN compounds c ON c.project_id = rp.project_id
JOIN screening_results sr ON sr.compound_id = c.compound_id
GROUP BY rp.project_id, rp.project_code;

-- Materialized view: same aggregation, but the underlying join is expensive and the
-- dashboard is read far more often than the data changes -- trade staleness for latency.
CREATE MATERIALIZED VIEW mv_assay_hit_counts AS
SELECT
    a.assay_id,
    a.assay_name,
    COUNT(*) AS total_results,
    COUNT(*) FILTER (WHERE sr.is_hit) AS hits
FROM screening_results sr
JOIN screening_runs run ON run.screening_run_id = sr.screening_run_id
JOIN assays a ON a.assay_id = run.assay_id
GROUP BY a.assay_id, a.assay_name
WITH DATA;

-- A unique index is required on a materialized view before it can be refreshed
-- CONCURRENTLY (i.e. without blocking readers during the refresh).
CREATE UNIQUE INDEX uq_mv_assay_hit_counts_assay_id ON mv_assay_hit_counts (assay_id);

-- Concurrent refresh: readers see the old data until this commits, then atomically
-- switch to the new data -- no downtime, no empty-table window.
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_assay_hit_counts;
