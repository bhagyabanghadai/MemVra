package com.memvra.enums;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonValue;

public enum SourceType {
    USER_INPUT("user_input"),
    DOCUMENT("document"),
    API_RESPONSE("api_response"),
    AGENT_INFERENCE("agent_inference");

    private final String value;

    SourceType(String value) { this.value = value; }

    @JsonValue
    public String toValue() { return value; }

    @JsonCreator
    public static SourceType from(String raw) {
        if (raw == null) return null;
        String s = raw.trim().toLowerCase();
        for (SourceType st : values()) {
            if (st.value.equals(s)) return st;
        }
        throw new IllegalArgumentException("Invalid source_type: " + raw);
    }
}