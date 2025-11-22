package com.memvra.controller;

/**
 * Indicates a client-side input error that should result in HTTP 400.
 */
public class BadRequestException extends RuntimeException {
    public BadRequestException(String message) { super(message); }
}