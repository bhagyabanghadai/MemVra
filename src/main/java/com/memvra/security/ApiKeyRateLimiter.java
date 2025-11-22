package com.memvra.security;

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Simple per-API-key fixed window rate limiter (1-minute windows).
 */
public class ApiKeyRateLimiter {
    private static class WindowCounter {
        volatile long windowStartMs;
        final AtomicInteger count = new AtomicInteger(0);
        WindowCounter(long start) { this.windowStartMs = start; }
    }

    private final int limitPerMinute;
    private final ConcurrentHashMap<String, WindowCounter> counters = new ConcurrentHashMap<>();

    public ApiKeyRateLimiter(int limitPerMinute) {
        this.limitPerMinute = Math.max(1, limitPerMinute);
    }

    /** Returns true if the request is allowed; false if rate-limited. */
    public boolean allow(String apiKey) {
        long now = System.currentTimeMillis();
        WindowCounter wc = counters.computeIfAbsent(apiKey == null ? "__missing__" : apiKey, k -> new WindowCounter(now));
        // Reset window after 60s
        if (now - wc.windowStartMs >= 60_000) {
            wc.windowStartMs = now;
            wc.count.set(0);
        }
        int newCount = wc.count.incrementAndGet();
        return newCount <= limitPerMinute;
    }

    public int getLimitPerMinute() {
        return limitPerMinute;
    }
}