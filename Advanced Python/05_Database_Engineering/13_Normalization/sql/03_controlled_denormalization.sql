-- PRODUCTION TRADEOFF: the normalized form above requires a 4-table join for the
-- dashboard's single most frequent read (hit rate per target, refreshed every page load
-- at high traffic). Rather than renormalizing, add a deliberately denormalized,
-- mechanically refreshed summary table -- the normalized tables remain the source of
-- truth and the only write target; this table is disposable and rebuildable.
CREATE TABLE target_hit_rate_summary (
    target_id          BIGINT PRIMARY KEY REFERENCES molecular_targets(target_id),
    gene_symbol           TEXT NOT NULL,          -- denormalized copy, refreshed on schedule
    total_results            BIGINT NOT NULL,
    total_hits                  BIGINT NOT NULL,
    hit_rate_pct                   NUMERIC(5,2) NOT NULL,
    refreshed_at                      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE OR REPLACE FUNCTION refresh_target_hit_rate_summary() RETURNS void
LANGUAGE plpgsql AS $$
BEGIN
    TRUNCATE target_hit_rate_summary;
    INSERT INTO target_hit_rate_summary (target_id, gene_symbol, total_results, total_hits, hit_rate_pct)
    SELECT
        mt.target_id,
        mt.gene_symbol,
        COUNT(sr.screening_result_id),
        COUNT(sr.screening_result_id) FILTER (WHERE sr.potency_nm < 100),
        ROUND(
            COUNT(sr.screening_result_id) FILTER (WHERE sr.potency_nm < 100)::NUMERIC
            / NULLIF(COUNT(sr.screening_result_id), 0) * 100, 2
        )
    FROM molecular_targets mt
    JOIN screening_runs run ON run.target_id = mt.target_id
    JOIN screening_results sr ON sr.screening_run_id = run.screening_run_id
    GROUP BY mt.target_id, mt.gene_symbol;
END;
$$;
