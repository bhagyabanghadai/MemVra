package com.memvra.security;

import io.micrometer.core.instrument.simple.SimpleMeterRegistry;
import org.junit.jupiter.api.Test;
import org.springframework.mock.web.MockFilterChain;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.mock.web.MockHttpServletResponse;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

public class ApiKeyAuthFilterTest {

    @Test
    void missingApiKeyReturns401() throws Exception {
        ApiKeyAuthFilter filter = new ApiKeyAuthFilter("unit-test-key", List.of(), null, new SimpleMeterRegistry());
        MockHttpServletRequest request = new MockHttpServletRequest();
        request.setRequestURI("/any/path");
        MockHttpServletResponse response = new MockHttpServletResponse();
        MockFilterChain chain = new MockFilterChain();

        filter.doFilter(request, response, chain);

        assertEquals(401, response.getStatus());
        String body = response.getContentAsString();
        assertTrue(body.contains("UNAUTHORIZED"));
        assertTrue(body.contains("Missing or invalid API key"));
    }

    @Test
    void validApiKeyContinuesChain() throws Exception {
        ApiKeyAuthFilter filter = new ApiKeyAuthFilter("unit-test-key", List.of(), null, new SimpleMeterRegistry());
        MockHttpServletRequest request = new MockHttpServletRequest();
        request.setRequestURI("/any/path");
        request.addHeader("X-API-Key", "unit-test-key");
        MockHttpServletResponse response = new MockHttpServletResponse();
        MockFilterChain chain = new MockFilterChain();

        filter.doFilter(request, response, chain);

        assertEquals(200, response.getStatus());
        assertEquals("", response.getContentAsString());
    }

    @Test
    void excludedPathBypassesAuth() throws Exception {
        ApiKeyAuthFilter filter = new ApiKeyAuthFilter("unit-test-key", List.of("/swagger-ui/**"), null, new SimpleMeterRegistry());
        MockHttpServletRequest request = new MockHttpServletRequest();
        request.setRequestURI("/swagger-ui/index.html");
        MockHttpServletResponse response = new MockHttpServletResponse();
        MockFilterChain chain = new MockFilterChain();

        filter.doFilter(request, response, chain);

        assertEquals(200, response.getStatus());
    }

    @Test
    void rateLimitBlocksExcessRequests() throws Exception {
        ApiKeyRateLimiter limiter = new ApiKeyRateLimiter(1); // allow 1 per minute
        ApiKeyAuthFilter filter = new ApiKeyAuthFilter("unit-test-key", List.of(), limiter, new SimpleMeterRegistry());
        MockHttpServletRequest req1 = new MockHttpServletRequest();
        req1.setRequestURI("/any/path");
        req1.setMethod("POST");
        req1.addHeader("X-API-Key", "unit-test-key");
        MockHttpServletResponse res1 = new MockHttpServletResponse();
        MockFilterChain chain1 = new MockFilterChain();
        filter.doFilter(req1, res1, chain1); // first allowed

        MockHttpServletRequest req2 = new MockHttpServletRequest();
        req2.setRequestURI("/any/path");
        req2.setMethod("POST");
        req2.addHeader("X-API-Key", "unit-test-key");
        MockHttpServletResponse res2 = new MockHttpServletResponse();
        MockFilterChain chain2 = new MockFilterChain();

        filter.doFilter(req2, res2, chain2);
        assertEquals(429, res2.getStatus());
        String body = res2.getContentAsString();
        assertTrue(body.contains("Rate limit exceeded"));
        String retryAfter = res2.getHeader("Retry-After");
        assertNotNull(retryAfter);
        assertTrue(Integer.parseInt(retryAfter) > 0);
    }
}