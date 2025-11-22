package com.memvra.controller;

import com.memvra.model.ApiKey;
import com.memvra.service.ApiKeyService;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/v1/dashboard")
public class DashboardController {

    private final ApiKeyService apiKeyService;

    public DashboardController(ApiKeyService apiKeyService) {
        this.apiKeyService = apiKeyService;
    }

    @GetMapping("/keys")
    public ResponseEntity<List<ApiKey>> listKeys(Authentication authentication) {
        return ResponseEntity.ok(apiKeyService.getUserKeys(authentication.getName()));
    }

    @PostMapping("/keys")
    public ResponseEntity<Map<String, String>> createKey(Authentication authentication, @RequestBody Map<String, String> request) {
        String name = request.get("name");
        if (name == null || name.isBlank()) {
            return ResponseEntity.badRequest().build();
        }
        String rawKey = apiKeyService.createApiKey(authentication.getName(), name);
        return ResponseEntity.ok(Map.of("key", rawKey));
    }

    @DeleteMapping("/keys/{id}")
    public ResponseEntity<Void> revokeKey(Authentication authentication, @PathVariable UUID id) {
        apiKeyService.revokeKey(authentication.getName(), id);
        return ResponseEntity.noContent().build();
    }
}
