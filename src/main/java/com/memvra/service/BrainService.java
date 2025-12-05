package com.memvra.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;

import java.util.List;
import java.util.Map;

@Service
public class BrainService {

    @Value("${memvra.brain.url}")
    private String brainUrl;

    private final RestTemplate restTemplate;

    public BrainService() {
        this.restTemplate = new RestTemplate();
    }

    public String recallLogicalFact(String query) {
        try {
            String url = brainUrl + "/v1/logical/recall?query=" + query;
            ResponseEntity<Map> response = restTemplate.postForEntity(url, null, Map.class);
            return (String) response.getBody().get("result");
        } catch (Exception e) {
            return "Logical Brain unavailable: " + e.getMessage();
        }
    }

    public Map<String, Object> triggerDreamCycle(List<Map<String, Object>> facts) {
        try {
            String url = brainUrl + "/v1/intuitive/dream";
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            Map<String, Object> request = Map.of("facts", facts);
            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(request, headers);

            ResponseEntity<Map> response = restTemplate.postForEntity(url, entity, Map.class);
            return response.getBody();
        } catch (Exception e) {
            return Map.of("error", "Intuitive Brain unavailable: " + e.getMessage());
        }
    }
}
