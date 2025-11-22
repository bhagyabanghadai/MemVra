-- Add revocation columns to support soft invalidation of facts
ALTER TABLE fact_records
ADD COLUMN revoked BOOLEAN NOT NULL DEFAULT FALSE,
ADD COLUMN revocation_reason TEXT,
ADD COLUMN revoked_at TIMESTAMPTZ;

CREATE INDEX idx_fact_records_revoked ON fact_records(revoked);
