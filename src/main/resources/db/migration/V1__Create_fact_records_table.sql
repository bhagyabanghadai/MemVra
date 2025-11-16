CREATE TABLE IF NOT EXISTS fact_records (
    fact_id UUID PRIMARY KEY,
    content TEXT NOT NULL,
    source_type VARCHAR(50) NOT NULL,
    source_id TEXT NOT NULL,
    recorded_by VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    signature BYTEA NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_fact_records_source_type ON fact_records(source_type);
CREATE INDEX IF NOT EXISTS idx_fact_records_recorded_by ON fact_records(recorded_by);
CREATE INDEX IF NOT EXISTS idx_fact_records_created_at ON fact_records(created_at);
CREATE INDEX IF NOT EXISTS idx_fact_records_source_id ON fact_records(source_id);

COMMENT ON TABLE fact_records IS 'Immutable ledger of verified facts with cryptographic signatures';