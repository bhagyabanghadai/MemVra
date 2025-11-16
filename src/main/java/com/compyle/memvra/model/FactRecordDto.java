package com.compyle.memvra.model;

import com.compyle.memvra.enums.SourceType;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.time.OffsetDateTime;

public class FactRecordDto {
    @JsonProperty("fact_id")
    private String factId;
    private String content;
    @JsonProperty("source_type")
    private SourceType sourceType;
    @JsonProperty("source_id")
    private String sourceId;
    @JsonProperty("recorded_by")
    private String recordedBy;
    @JsonProperty("created_at")
    private OffsetDateTime createdAt;
    private String signature;

    public FactRecordDto(String factId, String content, SourceType sourceType, String sourceId,
                         String recordedBy, OffsetDateTime createdAt, String signature) {
        this.factId = factId;
        this.content = content;
        this.sourceType = sourceType;
        this.sourceId = sourceId;
        this.recordedBy = recordedBy;
        this.createdAt = createdAt;
        this.signature = signature;
    }

    public String getFactId() { return factId; }
    public String getContent() { return content; }
    public SourceType getSourceType() { return sourceType; }
    public String getSourceId() { return sourceId; }
    public String getRecordedBy() { return recordedBy; }
    public OffsetDateTime getCreatedAt() { return createdAt; }
    public String getSignature() { return signature; }
}