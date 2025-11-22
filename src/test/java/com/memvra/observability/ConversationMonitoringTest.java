package com.memvra.observability;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.slf4j.LoggerFactory;
import ch.qos.logback.classic.Logger;
import ch.qos.logback.classic.spi.ILoggingEvent;
import ch.qos.logback.core.read.ListAppender;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.system.CapturedOutput;
import org.springframework.boot.test.system.OutputCaptureExtension;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;

import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

import java.util.Map;
import java.util.UUID;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Testcontainers
@ExtendWith(OutputCaptureExtension.class)
public class ConversationMonitoringTest {

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
        registry.add("memvra.fact.secret-key", () -> "test-secret-key-1234567890");
        // Ensure API key is disabled in this test to simplify calls
        registry.add("memvra.security.api-key.enabled", () -> "false");
    }

    @LocalServerPort
    int port;

    @Autowired
    TestRestTemplate rest;

    @Test
    void conversationTranscriptAndMonitoring(CapturedOutput output) {
        // Capture logs programmatically from specific loggers
        Logger reqLogger = (Logger) LoggerFactory.getLogger(com.memvra.security.RequestLoggingFilter.class);
        ListAppender<ILoggingEvent> reqAppender = new ListAppender<>();
        reqAppender.start();
        reqLogger.addAppender(reqAppender);

        Logger gehLogger = (Logger) LoggerFactory.getLogger(com.memvra.controller.GlobalExceptionHandler.class);
        ListAppender<ILoggingEvent> gehAppender = new ListAppender<>();
        gehAppender.start();
        gehLogger.addAppender(gehAppender);

        String base = "http://localhost:" + port;
        String cid = "test-cid-123";

        Map<String, Object> reqBody = Map.of(
                "content", "Agent reports: Berlin is the capital of Germany",
                "source_type", "user_input",
                "source_id", "chat:session_demo:turn_1",
                "recorded_by", "monitoring-agent-v1"
        );

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        headers.add("X-Correlation-Id", cid);

        // Step 1: Create a fact (201)
        ResponseEntity<Map> created = rest.postForEntity(base + "/v1/facts", new HttpEntity<>(reqBody, headers), Map.class);
        assert created.getStatusCode().equals(HttpStatus.CREATED);
        String factId = (String) created.getBody().get("fact_id");
        assert factId != null && factId.startsWith("mv-");
        // Response echoes correlation id
        String echoedCid = created.getHeaders().getFirst("X-Correlation-Id");
        assert cid.equals(echoedCid);

        // Step 2: Duplicate submission (409)
        ResponseEntity<Map> duplicate = rest.postForEntity(base + "/v1/facts", new HttpEntity<>(reqBody, headers), Map.class);
        assert duplicate.getStatusCode().value() == 409;
        Map<?,?> err = duplicate.getBody();
        assert err != null;
        // ErrorResponse serializes the error code under key 'error'
        assert "CONFLICT".equals(err.get("error"));

        // Step 3: Fetch by id (200)
        ResponseEntity<Map> fetched = rest.getForEntity(base + "/v1/facts/" + factId, Map.class);
        assert fetched.getStatusCode().equals(HttpStatus.OK);
        Map<?,?> fact = fetched.getBody();
        assert fact != null;
        assert factId.equals(fact.get("fact_id"));

        // Step 4: Health endpoint (200)
        ResponseEntity<Map> health = rest.getForEntity(base + "/actuator/health", Map.class);
        assert health.getStatusCode().equals(HttpStatus.OK);
        assert health.getBody() != null && health.getBody().containsKey("status");

        // Verify request logging events
        boolean sawCreate = reqAppender.list.stream().anyMatch(e -> e.getFormattedMessage().contains("req method=POST uri=/v1/facts") && e.getFormattedMessage().contains("status=201"));
        boolean sawConflict = reqAppender.list.stream().anyMatch(e -> e.getFormattedMessage().contains("req method=POST uri=/v1/facts") && e.getFormattedMessage().contains("status=409"));
        boolean sawCreateText = output.getOut().contains("req method=POST uri=/v1/facts") && output.getOut().contains("status=201");
        boolean sawConflictText = output.getOut().contains("req method=POST uri=/v1/facts") && output.getOut().contains("status=409");
        assert sawCreate || sawCreateText;
        assert sawConflict || sawConflictText;

        // Verify GlobalExceptionHandler logged the conflict
        boolean gehLoggedConflict = gehAppender.list.stream().anyMatch(e -> e.getFormattedMessage().contains("Conflict:"));
        assert gehLoggedConflict || output.getOut().contains("Conflict:");

        // Cleanup appenders
        reqLogger.detachAppender(reqAppender);
        gehLogger.detachAppender(gehAppender);
    }
}