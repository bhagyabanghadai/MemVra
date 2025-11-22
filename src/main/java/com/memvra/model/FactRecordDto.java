package com.memvra.model;

import com.memvra.enums.SourceType;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.time.OffsetDateTime;

public record FactRecordDto(
    @JsonProperty("fact_id") String factId,
    String content,
    @JsonProperty("source_type") SourceType sourceType,
    @JsonProperty("source_id") String sourceId,
    @JsonProperty("recorded_by") String recordedBy,
    @JsonProperty("created_at") OffsetDateTime createdAt,
    String signature,
    boolean revoked,
    @JsonProperty("revocation_reason") String revocationReason,
    @JsonProperty("revoked_at") OffsetDateTime revokedAt
) {}