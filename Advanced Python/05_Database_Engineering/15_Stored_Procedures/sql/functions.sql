-- Set-returning function: computes potency percentile rank for a target, entirely
-- database-side because it needs a window function over potentially millions of rows --
-- shipping that data to Python just to rank it would be wasteful.
CREATE OR REPLACE FUNCTION fn_compound_potency_percentile(p_target_id BIGINT)
RETURNS TABLE (compound_id BIGINT, potency_nm NUMERIC, percentile NUMERIC)
LANGUAGE sql STABLE AS $$
    SELECT
        c.compound_id,
        sr.potency_nm,
        ROUND(PERCENT_RANK() OVER (ORDER BY sr.potency_nm)::NUMERIC, 4)
    FROM compounds c
    JOIN screening_results sr ON sr.compound_id = c.compound_id
    JOIN screening_runs run ON run.screening_run_id = sr.screening_run_id
    JOIN assays a ON a.assay_id = run.assay_id
    WHERE a.target_id = p_target_id AND sr.potency_nm IS NOT NULL;
$$;

-- Scalar function with input validation: database-side computation of a derived,
-- frequently-filtered value (drug-likeness heuristic), computed once at write time
-- rather than recomputed by every reader.
CREATE OR REPLACE FUNCTION fn_lipinski_violations(
    p_molecular_weight NUMERIC,
    p_logp NUMERIC,
    p_hbd INTEGER,
    p_hba INTEGER
) RETURNS INTEGER
LANGUAGE plpgsql IMMUTABLE AS $$
DECLARE
    v_violations INTEGER := 0;
BEGIN
    IF p_molecular_weight IS NULL OR p_logp IS NULL OR p_hbd IS NULL OR p_hba IS NULL THEN
        RAISE EXCEPTION 'fn_lipinski_violations: all four parameters are required, got NULL';
    END IF;

    IF p_molecular_weight > 500 THEN v_violations := v_violations + 1; END IF;
    IF p_logp > 5 THEN v_violations := v_violations + 1; END IF;
    IF p_hbd > 5 THEN v_violations := v_violations + 1; END IF;
    IF p_hba > 10 THEN v_violations := v_violations + 1; END IF;

    RETURN v_violations;
END;
$$;
