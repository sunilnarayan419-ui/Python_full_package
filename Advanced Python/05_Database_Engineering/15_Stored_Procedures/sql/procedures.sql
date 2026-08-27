-- Procedure with explicit transaction control and structured exception handling.
-- Used for a multi-step archival operation that must be all-or-nothing and must
-- report a clear, specific error rather than a raw constraint violation.
CREATE OR REPLACE PROCEDURE sp_archive_completed_project(p_project_id BIGINT)
LANGUAGE plpgsql AS $$
DECLARE
    v_status TEXT;
BEGIN
    SELECT status INTO v_status FROM research_projects WHERE project_id = p_project_id FOR UPDATE;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'sp_archive_completed_project: project % does not exist', p_project_id
            USING ERRCODE = 'no_data_found';
    END IF;

    IF v_status <> 'completed' THEN
        RAISE EXCEPTION 'sp_archive_completed_project: project % is not completed (status=%)',
            p_project_id, v_status
            USING ERRCODE = 'check_violation';
    END IF;

    UPDATE research_projects SET deleted_at = now() WHERE project_id = p_project_id;

    INSERT INTO project_archive_log (project_id, archived_at)
    VALUES (p_project_id, now());

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
$$;
