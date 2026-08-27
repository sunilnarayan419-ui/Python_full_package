-- POOR: unnormalized. Repeats researcher and target attributes on every row,
-- causing update/insertion/deletion anomalies.
CREATE TABLE screening_results_denormalized (
    screening_result_id     BIGSERIAL PRIMARY KEY,
    compound_smiles           TEXT NOT NULL,
    compound_molecular_weight   NUMERIC(10,4) NOT NULL,
    researcher_name                TEXT NOT NULL,
    researcher_email                 TEXT NOT NULL,      -- repeated per result: update anomaly
    target_gene_symbol                  TEXT NOT NULL,       -- repeated per result: update anomaly
    target_uniprot_accession               TEXT NOT NULL,
    potency_nm                                NUMERIC(12,4),
    run_date                                    DATE NOT NULL
);
-- Anomalies:
-- Update: fixing a researcher's email requires updating every result row they touched.
-- Insertion: cannot record a new researcher until they have produced a screening result.
-- Deletion: deleting the last result for a target silently deletes all knowledge of that target.
