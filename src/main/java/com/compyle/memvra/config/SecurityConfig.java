package com.compyle.memvra.config;

import com.compyle.memvra.security.ApiKeyAuthFilter;
import com.compyle.memvra.security.CorrelationIdFilter;
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
    @ConditionalOnProperty(prefix = "compyle.security.api-key", name = "enabled", havingValue = "true")
    public FilterRegistrationBean<ApiKeyAuthFilter> apiKeyAuthFilter(ApiKeyProperties props) {
        FilterRegistrationBean<ApiKeyAuthFilter> reg = new FilterRegistrationBean<>();
        reg.setFilter(new ApiKeyAuthFilter(props.getValue()));
        // After correlation id filter
        reg.setOrder(Ordered.HIGHEST_PRECEDENCE + 1);
        return reg;
    }

    @ConfigurationProperties(prefix = "compyle.security.api-key")
    public static class ApiKeyProperties {
        private boolean enabled = false;
        private String value = "";

        public boolean isEnabled() { return enabled; }
        public void setEnabled(boolean enabled) { this.enabled = enabled; }
        public String getValue() { return value; }
        public void setValue(String value) { this.value = value; }
    }
}