package com.compyle.memvra.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.time.OffsetDateTime;

public class ErrorResponse {
    private final String error;
    private final String message;
    private final String field;
    @JsonProperty("timestamp")
    private final OffsetDateTime timestamp;

    public ErrorResponse(String error, String message, String field) {
        this.error = error;
        this.message = message;
        this.field = field;
        this.timestamp = OffsetDateTime.now();
    }

    public String getError() { return error; }
    public String getMessage() { return message; }
    public String getField() { return field; }
    public OffsetDateTime getTimestamp() { return timestamp; }
}