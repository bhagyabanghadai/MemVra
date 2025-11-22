package com.memvra.security;

/**
 * Thrown when an incoming request is missing a valid API key.
 */
public class ApiKeyAuthenticationException extends RuntimeException {
    public ApiKeyAuthenticationException(String message) {
        super(message);
    }
}