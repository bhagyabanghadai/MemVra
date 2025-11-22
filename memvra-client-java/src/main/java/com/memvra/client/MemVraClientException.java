package com.memvra.client;

public class MemVraClientException extends RuntimeException {
    private final String code;

    public MemVraClientException(String code, String message, Throwable cause) {
        super(message, cause);
        this.code = code;
    }

    public String getCode() { return code; }
}