package com.compyle.memvra.client;

public class Fact {
    private String content;
    private SourceType sourceType;
    private String sourceId;
    private String recordedBy;

    public Fact(String content) { this.content = content; }

    public Fact withSource(SourceType type, String sourceId) {
        this.sourceType = type;
        this.sourceId = sourceId;
        return this;
    }

    public Fact recordedBy(String recordedBy) {
        this.recordedBy = recordedBy;
        return this;
    }

    public String getContent() { return content; }
    public SourceType getSourceType() { return sourceType; }
    public String getSourceId() { return sourceId; }
    public String getRecordedBy() { return recordedBy; }
}