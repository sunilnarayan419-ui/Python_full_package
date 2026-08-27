-- SELECT ... FOR UPDATE SKIP LOCKED: safe queue-style claiming of samples
BEGIN;
SELECT sample_id, status
FROM samples
WHERE status = 'sequenced'
ORDER BY created_at
LIMIT 10
FOR UPDATE SKIP LOCKED;

UPDATE samples SET status = 'analyzed' WHERE sample_id = ANY($1::uuid[]);
COMMIT;

-- Serializable isolation for a balance-sensitive style operation
BEGIN ISOLATION LEVEL SERIALIZABLE;
SELECT read_count FROM gene_expression_reads WHERE sample_id = $1 AND gene_id = $2 FOR UPDATE;
UPDATE gene_expression_reads SET read_count = read_count + $3 WHERE sample_id = $1 AND gene_id = $2;
COMMIT;
