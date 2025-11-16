package com.compyle.memvra.integration;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;

import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.Map;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Testcontainers
public class FactApiIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15")
            .withDatabaseName("memvra")
            .withUsername("memvra")
            .withPassword("password");

    @DynamicPropertySource
    static void registerProps(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
        registry.add("compyle.fact.secret-key", () -> "test-secret-key-1234567890");
    }

    @LocalServerPort
    int port;

    @Autowired
    TestRestTemplate rest;

    @Test
    void recordAndVerifySignature() throws Exception {
        String base = "http://localhost:" + port;

        Map<String, Object> reqBody = Map.of(
                "content", "Integration test fact",
                "source_type", "user_input",
                "source_id", "itest:source:1",
                "recorded_by", "itest-agent"
        );

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        ResponseEntity<Map> created = rest.postForEntity(base + "/v1/facts", new HttpEntity<>(reqBody, headers), Map.class);

        assert created.getStatusCode().is2xxSuccessful();
        String factId = (String) created.getBody().get("fact_id");

        ResponseEntity<Map> fetched = rest.getForEntity(base + "/v1/facts/" + factId, Map.class);
        assert fetched.getStatusCode().is2xxSuccessful();
        Map<?,?> fact = fetched.getBody();

        String payload = fact.get("fact_id") + "|" + fact.get("content") + "|" + fact.get("source_type") + "|" +
                fact.get("source_id") + "|" + fact.get("recorded_by") + "|" + fact.get("created_at");
        Mac hmac = Mac.getInstance("HmacSHA256");
        hmac.init(new SecretKeySpec("test-secret-key-1234567890".getBytes(StandardCharsets.UTF_8), "HmacSHA256"));
        String computed = Base64.getEncoder().encodeToString(hmac.doFinal(payload.getBytes(StandardCharsets.UTF_8)));

        String serverSig = (String) fact.get("signature");
        assert computed.equals(serverSig);
    }
}