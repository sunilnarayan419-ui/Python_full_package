-- Every index above adds write overhead: each INSERT/UPDATE touching an indexed column
-- must also update that index's B-tree/GIN structure. Before adding an index, confirm
-- it serves a query on the hot read path -- verify with pg_stat_user_indexes idx_scan
-- counts on a representative workload, and drop indexes whose idx_scan stays at 0.
SELECT
    schemaname, relname, indexrelname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
WHERE relname = 'compounds'
ORDER BY idx_scan ASC;
