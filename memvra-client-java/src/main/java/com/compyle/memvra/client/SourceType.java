package com.compyle.memvra.client;

public enum SourceType {
    USER_INPUT("user_input"),
    DOCUMENT("document"),
    API_RESPONSE("api_response"),
    AGENT_INFERENCE("agent_inference");

    private final String value;
    SourceType(String value) { this.value = value; }
    public String value() { return value; }
}