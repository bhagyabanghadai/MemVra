package com.memvra.service;

import com.memvra.model.ApiKey;
import com.memvra.model.User;
import com.memvra.repository.ApiKeyRepository;
import com.memvra.repository.UserRepository;
import org.apache.commons.codec.digest.DigestUtils;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.security.SecureRandom;
import java.time.OffsetDateTime;
import java.util.Base64;
import java.util.List;
import java.util.UUID;

@Service
public class ApiKeyService {

    private final ApiKeyRepository apiKeyRepository;
    private final UserRepository userRepository;
    private final SecureRandom secureRandom = new SecureRandom();

    public ApiKeyService(ApiKeyRepository apiKeyRepository, UserRepository userRepository) {
        this.apiKeyRepository = apiKeyRepository;
        this.userRepository = userRepository;
    }

    public List<ApiKey> getUserKeys(String email) {
        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new RuntimeException("User not found"));
        return apiKeyRepository.findByUserUserId(user.getUserId());
    }

    @Transactional
    public String createApiKey(String email, String name) {
        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new RuntimeException("User not found"));

        // Generate random key
        byte[] randomBytes = new byte[24];
        secureRandom.nextBytes(randomBytes);
        String rawKey = "mv_sk_" + Base64.getUrlEncoder().withoutPadding().encodeToString(randomBytes);

        // Hash key
        String keyHash = DigestUtils.sha256Hex(rawKey);

        ApiKey apiKey = new ApiKey();
        apiKey.setKeyId(UUID.randomUUID());
        apiKey.setKeyHash(keyHash);
        apiKey.setName(name);
        apiKey.setUser(user);
        apiKey.setCreatedAt(OffsetDateTime.now());
        
        apiKeyRepository.save(apiKey);

        return rawKey; // Return raw key only once
    }

    @Transactional
    public void revokeKey(String email, UUID keyId) {
        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new RuntimeException("User not found"));
        
        ApiKey apiKey = apiKeyRepository.findById(keyId)
                .orElseThrow(() -> new RuntimeException("Key not found"));

        if (!apiKey.getUser().getUserId().equals(user.getUserId())) {
            throw new RuntimeException("Unauthorized access to key");
        }

        apiKey.setRevoked(true);
        apiKeyRepository.save(apiKey);
    }
}
