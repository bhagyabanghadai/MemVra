package com.memvra.client;

import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.web.client.HttpServerErrorException;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestTemplate;

import java.util.Map;
import java.util.Objects;
import java.util.function.Supplier;

public class MemVraClient {
    private final String baseUrl;
    private final String apiKey; // optional for future auth
    private final RestTemplate restTemplate;
    private final int maxRetries;
    private final int retryBackoffMs;

    private MemVraClient(String baseUrl, String apiKey, int connectTimeoutMs, int readTimeoutMs, int maxRetries, int retryBackoffMs) {
        this.baseUrl = Objects.requireNonNull(baseUrl, "baseUrl");
        this.apiKey = apiKey;
        this.maxRetries = Math.max(0, maxRetries);
        this.retryBackoffMs = Math.max(0, retryBackoffMs);
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        factory.setConnectTimeout(connectTimeoutMs);
        factory.setReadTimeout(readTimeoutMs);
        this.restTemplate = new RestTemplate(factory);
    }

    public static Builder builder() { return new Builder(); }

    public static class Builder {
        private String baseUrl;
        private String apiKey;
        private int connectTimeoutMs = 3000;
        private int readTimeoutMs = 5000;
        private int maxRetries = 0;
        private int retryBackoffMs = 0;

        public Builder baseUrl(String baseUrl) { this.baseUrl = baseUrl; return this; }
        public Builder apiKey(String apiKey) { this.apiKey = apiKey; return this; }
        public Builder connectTimeoutMs(int ms) { this.connectTimeoutMs = ms; return this; }
        public Builder readTimeoutMs(int ms) { this.readTimeoutMs = ms; return this; }
        public Builder maxRetries(int retries) { this.maxRetries = retries; return this; }
        public Builder retryBackoffMs(int ms) { this.retryBackoffMs = ms; return this; }
        public MemVraClient build() {
            return new MemVraClient(baseUrl, apiKey, connectTimeoutMs, readTimeoutMs, maxRetries, retryBackoffMs);
        }
    }

    public Map<?,?> record(Fact fact) {
        HttpHeaders headers = defaultHeaders();
        HttpEntity<Map<String, Object>> req = new HttpEntity<>(Map.of(
                "content", fact.getContent(),
                "source_type", fact.getSourceType().value(),
                "source_id", fact.getSourceId(),
                "recorded_by", fact.getRecordedBy()
        ), headers);
        try {
            return restTemplate.postForObject(baseUrl + "/v1/facts", req, Map.class);
        } catch (Exception e) {
            throw new MemVraClientException("REQUEST_FAILED", "Failed to record fact", e);
        }
    }

    public Map<?,?> getFact(String factId) {
        HttpHeaders headers = defaultHeaders();
        HttpEntity<Void> req = new HttpEntity<>(headers);
        return withRetry(() -> restTemplate.exchange(baseUrl + "/v1/facts/" + factId, org.springframework.http.HttpMethod.GET, req, Map.class).getBody());
    }

    public boolean verify(String factId, String secretKey) {
        Map<?,?> fact = getFact(factId);
        if (fact == null) return false;

        String externalId = (String) fact.get("fact_id");
        String content = (String) fact.get("content");
        String sourceType = (String) fact.get("source_type");
        String sourceId = (String) fact.get("source_id");
        String recordedBy = (String) fact.get("recorded_by");
        String createdAt = String.valueOf(fact.get("created_at"));
        String signatureBase64 = (String) fact.get("signature");

        String payload = externalId + "|" + content + "|" + sourceType + "|" + sourceId + "|" + recordedBy + "|" + createdAt;

        try {
            javax.crypto.Mac hmac = javax.crypto.Mac.getInstance("HmacSHA256");
            javax.crypto.spec.SecretKeySpec keySpec = new javax.crypto.spec.SecretKeySpec(secretKey.getBytes(java.nio.charset.StandardCharsets.UTF_8), "HmacSHA256");
            hmac.init(keySpec);
            byte[] computed = hmac.doFinal(payload.getBytes(java.nio.charset.StandardCharsets.UTF_8));
            String computedBase64 = java.util.Base64.getEncoder().encodeToString(computed);
            return computedBase64.equals(signatureBase64);
        } catch (Exception e) {
            throw new MemVraClientException("VERIFY_FAILED", "Failed to verify HMAC signature", e);
        }
    }

    private HttpHeaders defaultHeaders() {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        if (apiKey != null && !apiKey.isBlank()) {
            headers.add("X-API-Key", apiKey);
        }
        return headers;
    }

    private <T> T withRetry(Supplier<T> action) {
        int attempt = 0;
        while (true) {
            try {
                return action.get();
            } catch (ResourceAccessException | HttpServerErrorException ex) {
                if (attempt >= maxRetries) {
                    throw new MemVraClientException("RETRY_EXHAUSTED", "Request failed after retries", ex);
                }
                attempt++;
                if (retryBackoffMs > 0) {
                    try { Thread.sleep(retryBackoffMs); } catch (InterruptedException ignored) { }
                }
            }
        }
    }
}