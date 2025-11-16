package com.compyle.memvra.model;

import com.compyle.memvra.enums.SourceType;
import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public class CreateFactRequest {

    @NotBlank
    @Size(max = 1000)
    private String content;

    @JsonProperty("source_type")
    private SourceType sourceType;

    @JsonProperty("source_id")
    @NotBlank
    private String sourceId;

    @JsonProperty("recorded_by")
    @NotBlank
    @Size(max = 100)
    private String recordedBy;

    public String getContent() { return content; }
    public void setContent(String content) { this.content = content == null ? null : content.trim(); }

    public SourceType getSourceType() { return sourceType; }
    public void setSourceType(SourceType sourceType) { this.sourceType = sourceType; }

    public String getSourceId() { return sourceId; }
    public void setSourceId(String sourceId) { this.sourceId = sourceId == null ? null : sourceId.trim(); }

    public String getRecordedBy() { return recordedBy; }
    public void setRecordedBy(String recordedBy) { this.recordedBy = recordedBy == null ? null : recordedBy.trim(); }
}