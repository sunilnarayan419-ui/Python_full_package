-- Wrapping the refresh in a function makes it schedulable (pg_cron, external scheduler,
-- or an application-level periodic task) and gives a single point to add logging/metrics.
CREATE OR REPLACE FUNCTION refresh_assay_hit_counts() RETURNS void
LANGUAGE plpgsql AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_assay_hit_counts;
EXCEPTION
    WHEN OTHERS THEN
        RAISE WARNING 'refresh_assay_hit_counts failed: %', SQLERRM;
        RAISE;
END;
$$;
