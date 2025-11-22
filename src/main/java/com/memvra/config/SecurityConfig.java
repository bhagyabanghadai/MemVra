package com.memvra.config;

import com.memvra.security.ApiKeyAuthFilter;
import com.memvra.security.ApiKeyRateLimiter;
import com.memvra.security.CorrelationIdFilter;
import com.memvra.security.RequestLoggingFilter;
import io.micrometer.core.instrument.MeterRegistry;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.Ordered;
import org.springframework.core.annotation.Order;
import org.springframework.boot.web.servlet.FilterRegistrationBean;

@Configuration
@EnableConfigurationProperties(SecurityConfig.ApiKeyProperties.class)
public class SecurityConfig {

    @Bean
    @Order(Ordered.HIGHEST_PRECEDENCE)
    public FilterRegistrationBean<CorrelationIdFilter> correlationIdFilter() {
        FilterRegistrationBean<CorrelationIdFilter> reg = new FilterRegistrationBean<>();
        reg.setFilter(new CorrelationIdFilter());
        reg.setOrder(Ordered.HIGHEST_PRECEDENCE);
        return reg;
    }

    @Bean
    @ConditionalOnProperty(prefix = "memvra.security.api-key", name = "enabled", havingValue = "true")
    public FilterRegistrationBean<ApiKeyAuthFilter> apiKeyAuthFilter(ApiKeyProperties props, MeterRegistry meterRegistry) {
        FilterRegistrationBean<ApiKeyAuthFilter> reg = new FilterRegistrationBean<>();
        ApiKeyRateLimiter limiter = props.getRateLimitPerMinute() > 0 ? new ApiKeyRateLimiter(props.getRateLimitPerMinute()) : null;
        reg.setFilter(new ApiKeyAuthFilter(props.getValue(), props.getExcludePaths(), limiter, meterRegistry));
        // After correlation id filter
        reg.setOrder(Ordered.HIGHEST_PRECEDENCE + 1);
        return reg;
    }

    @Bean
    public FilterRegistrationBean<RequestLoggingFilter> requestLoggingFilter() {
        FilterRegistrationBean<RequestLoggingFilter> reg = new FilterRegistrationBean<>();
        reg.setFilter(new RequestLoggingFilter());
        reg.setOrder(Ordered.LOWEST_PRECEDENCE);
        return reg;
    }

    @ConfigurationProperties(prefix = "memvra.security.api-key")
    public static class ApiKeyProperties {
        private boolean enabled = false;
        private String value = "";
        private java.util.List<String> excludePaths = java.util.List.of("/swagger-ui/**", "/v3/api-docs/**", "/actuator/health");
        private int rateLimitPerMinute = 60;

        public boolean isEnabled() { return enabled; }
        public void setEnabled(boolean enabled) { this.enabled = enabled; }
        public String getValue() { return value; }
        public void setValue(String value) { this.value = value; }
        public java.util.List<String> getExcludePaths() { return excludePaths; }
        public void setExcludePaths(java.util.List<String> excludePaths) { this.excludePaths = excludePaths; }
        public int getRateLimitPerMinute() { return rateLimitPerMinute; }
        public void setRateLimitPerMinute(int rateLimitPerMinute) { this.rateLimitPerMinute = rateLimitPerMinute; }
    }
}