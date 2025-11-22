-- Enforce uniqueness to prevent duplicate facts for the same source and recorder
-- This guards against race conditions and ensures ledger integrity at the database level.
ALTER TABLE IF EXISTS fact_records
    ADD CONSTRAINT unique_fact_per_agent UNIQUE (content, source_id, recorded_by);