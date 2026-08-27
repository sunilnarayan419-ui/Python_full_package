CREATE TABLE sample_aliquots (
    sample_id   BIGINT PRIMARY KEY,
    volume_ul   INTEGER NOT NULL CHECK (volume_ul >= 0)
);
