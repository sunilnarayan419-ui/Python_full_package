-- Sequential scan baseline (no predicate index yet)
EXPLAIN ANALYZE
SELECT gene_id, tpm FROM gene_expression_reads WHERE tpm > 500;

-- After idx_expression_high_tpm exists, planner should prefer an index scan
EXPLAIN (ANALYZE, BUFFERS)
SELECT ger.gene_id, ger.tpm
FROM gene_expression_reads ger
WHERE ger.gene_id = '00000000-0000-0000-0000-000000000000' AND ger.tpm > 100;

-- JSONB containment query using GIN index
EXPLAIN ANALYZE
SELECT gene_id, symbol FROM genes WHERE annotations @> '{"pathway": "MAPK"}'::jsonb;

-- Full-text search plan
EXPLAIN ANALYZE
SELECT gene_id, symbol FROM genes WHERE annotation_search @@ plainto_tsquery('english', 'kinase signaling');
