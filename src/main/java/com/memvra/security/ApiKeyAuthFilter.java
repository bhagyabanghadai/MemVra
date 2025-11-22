package com.memvra.security;

import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.List;
import java.time.OffsetDateTime;

/**
 * API key authentication filter. When enabled, requires header 'X-API-Key'
 * to match the configured application property. Supports path exclusions and
 * basic per-key rate limiting.
 */
public class ApiKeyAuthFilter extends OncePerRequestFilter {

    private final String expectedApiKey;
    private final List<String> excludePaths;
    private final ApiKeyRateLimiter rateLimiter;
    private final Counter authFailures;
    private final Counter rateLimited;

    public ApiKeyAuthFilter(String expectedApiKey,
                            List<String> excludePaths,
                            ApiKeyRateLimiter rateLimiter,
                            MeterRegistry meterRegistry) {
        this.expectedApiKey = expectedApiKey;
        this.excludePaths = excludePaths;
        this.rateLimiter = rateLimiter;
        this.authFailures = meterRegistry != null ? meterRegistry.counter("security.auth.failures") : null;
        this.rateLimited = meterRegistry != null ? meterRegistry.counter("security.rate_limited") : null;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain) throws ServletException, IOException {
        String uri = request.getRequestURI();
        if (isExcluded(uri)) {
            filterChain.doFilter(request, response);
            return;
        }

        String apiKey = request.getHeader("X-API-Key");
        if (apiKey == null || apiKey.isBlank() || !apiKey.equals(expectedApiKey)) {
            if (authFailures != null) authFailures.increment();
            writeError(response, HttpServletResponse.SC_UNAUTHORIZED, "UNAUTHORIZED", "Missing or invalid API key", null);
            return;
        }

        // Rate limiting (writes only: POST/PUT/DELETE)
        String method = request.getMethod();
        boolean isWrite = !("GET".equalsIgnoreCase(method) || "HEAD".equalsIgnoreCase(method));
        if (isWrite && rateLimiter != null && !rateLimiter.allow(apiKey)) {
            if (rateLimited != null) rateLimited.increment();
            int retryAfter = 60; // fixed window duration
            writeError(response, 429, "RATE_LIMITED", "Rate limit exceeded", retryAfter);
            return;
        }

        filterChain.doFilter(request, response);
    }

    private void writeError(HttpServletResponse response, int status, String code, String message, Integer retryAfterSeconds) throws IOException {
        response.setStatus(status);
        response.setContentType("application/json");
        if (retryAfterSeconds != null) {
            response.setHeader("Retry-After", String.valueOf(retryAfterSeconds));
        }
        String ts = OffsetDateTime.now().toString();
        String json = String.format("{\"error\":\"%s\",\"message\":\"%s\",\"field\":null,\"timestamp\":\"%s\"}", code, escape(message), ts);
        response.getWriter().write(json);
    }

    private String escape(String s) {
        return s == null ? "" : s.replace("\\", "\\\\").replace("\"", "\\\"");
    }

    private boolean isExcluded(String uri) {
        if (excludePaths == null || excludePaths.isEmpty()) return false;
        for (String p : excludePaths) {
            if (p == null || p.isBlank()) continue;
            if (p.endsWith("/**")) {
                String prefix = p.substring(0, p.length() - 3);
                if (uri.startsWith(prefix)) return true;
            } else if (uri.equals(p) || uri.startsWith(p)) {
                return true;
            }
        }
        return false;
    }
}