package com.memvra.config;

import com.memvra.config.SecurityConfig.ApiKeyProperties;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Component;
import org.springframework.boot.context.event.ApplicationReadyEvent;

@Component
public class StartupSecurityChecks {
    private static final Logger log = LoggerFactory.getLogger(StartupSecurityChecks.class);

    private final String secretKey;
    private final ApiKeyProperties apiProps;

    public StartupSecurityChecks(@Value("${memvra.fact.secret-key}") String secretKey,
                                 ApiKeyProperties apiProps) {
        this.secretKey = secretKey;
        this.apiProps = apiProps;
    }

    @EventListener(ApplicationReadyEvent.class)
    public void verifySecurityConfiguration() {
        if (secretKey == null || secretKey.isBlank() || "default-dev-secret-change-in-production".equals(secretKey)) {
            log.error("Security: memvra.fact.secret-key is unset or using the insecure dev default. Configure a strong secret in production.");
        }

        if (apiProps.isEnabled()) {
            String val = apiProps.getValue();
            if (val == null || val.isBlank()) {
                log.error("Security: API key auth is enabled but memvra.security.api-key.value is empty.");
            }
            int limit = apiProps.getRateLimitPerMinute();
            if (limit <= 0) {
                log.warn("Security: API key rate limit is non-positive. Set memvra.security.api-key.rate-limit-per-minute to a sensible value.");
            }
        } else {
            log.warn("Security: API key auth is disabled. Enable it for non-local environments.");
        }
    }
}