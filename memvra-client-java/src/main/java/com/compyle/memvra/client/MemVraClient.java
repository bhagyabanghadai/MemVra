package com.compyle.memvra.client;

import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

public class MemVraClient {
    private final String baseUrl;
    private final String apiKey; // placeholder for future auth
    private final RestTemplate restTemplate = new RestTemplate();

    public MemVraClient(String baseUrl, String apiKey) {
        this.baseUrl = baseUrl;
        this.apiKey = apiKey;
    }

    public Map<?,?> record(Fact fact) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<Map<String, Object>> req = new HttpEntity<>(Map.of(
                "content", fact.getContent(),
                "source_type", fact.getSourceType().value(),
                "source_id", fact.getSourceId(),
                "recorded_by", fact.getRecordedBy()
        ), headers);

        return restTemplate.postForObject(baseUrl + "/v1/facts", req, Map.class);
    }

    public Map<?,?> getFact(String factId) {
        return restTemplate.getForObject(baseUrl + "/v1/facts/" + factId, Map.class);
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
            throw new IllegalStateException("Failed to verify HMAC signature", e);
        }
    }
}