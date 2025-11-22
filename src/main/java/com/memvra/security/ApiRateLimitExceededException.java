package com.memvra.security;

/**
 * Thrown when an API key exceeds the configured request rate limit.
 */
public class ApiRateLimitExceededException extends RuntimeException {
    private final int retryAfterSeconds;

    public ApiRateLimitExceededException(String message, int retryAfterSeconds) {
        super(message);
        this.retryAfterSeconds = retryAfterSeconds;
    }

    public int getRetryAfterSeconds() {
        return retryAfterSeconds;
    }
}