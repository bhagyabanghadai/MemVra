package com.memvra.config;

import com.memvra.security.ApiKeyAuthFilter;
import com.memvra.security.ApiKeyRateLimiter;
import com.memvra.security.CorrelationIdFilter;
import com.memvra.security.JwtAuthenticationFilter;
import com.memvra.security.RequestLoggingFilter;
import io.micrometer.core.instrument.MeterRegistry;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.Ordered;
import org.springframework.core.annotation.Order;
import org.springframework.http.HttpMethod;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.AuthenticationProvider;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.boot.web.servlet.FilterRegistrationBean;

import java.util.List;

@Configuration
@EnableWebSecurity
@EnableConfigurationProperties(SecurityConfig.ApiKeyProperties.class)
public class SecurityConfig {

    @Autowired
    private JwtAuthenticationFilter jwtAuthenticationFilter;

    @Autowired
    private UserDetailsService userDetailsService;

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http, ApiKeyProperties apiKeyProperties, MeterRegistry meterRegistry) throws Exception {
        http
            .csrf(AbstractHttpConfigurer::disable)
            .cors(AbstractHttpConfigurer::disable) // Handled by WebConfig or Gateway
            .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/v1/auth/**").permitAll()
                .requestMatchers("/actuator/**").permitAll()
                .requestMatchers("/v3/api-docs/**", "/swagger-ui/**", "/swagger-ui.html").permitAll()
                .requestMatchers("/v1/brain/**").permitAll() // Brain integration
                .requestMatchers(HttpMethod.GET, "/v1/facts/**").permitAll() // Public read access
                .requestMatchers("/v1/dashboard/**").authenticated() // JWT required
                .anyRequest().authenticated() // Everything else requires auth (API Key or JWT)
            )
            .authenticationProvider(authenticationProvider())
            .addFilterBefore(jwtAuthenticationFilter, UsernamePasswordAuthenticationFilter.class);

        // Add API Key Filter if enabled
        if (apiKeyProperties.isEnabled()) {
            ApiKeyRateLimiter limiter = apiKeyProperties.getRateLimitPerMinute() > 0 ? new ApiKeyRateLimiter(apiKeyProperties.getRateLimitPerMinute()) : null;
            // We add it before JWT filter so it can handle API key requests first?
            // Or we can add it after.
            // Actually, for endpoints that require API Key (like POST /facts), we need to ensure it runs.
            // But we also have JWT endpoints.
            // Let's add it before UsernamePasswordAuthenticationFilter.
            // Note: ApiKeyAuthFilter in this codebase is a generic Filter, not a Spring Security Filter.
            // But we can add it to the chain.
            http.addFilterBefore(new ApiKeyAuthFilter(apiKeyProperties.getValue(), apiKeyProperties.getExcludePaths(), limiter, meterRegistry), UsernamePasswordAuthenticationFilter.class);
        }

        return http.build();
    }

    @Bean
    public AuthenticationProvider authenticationProvider() {
        DaoAuthenticationProvider authProvider = new DaoAuthenticationProvider();
        authProvider.setUserDetailsService(userDetailsService);
        authProvider.setPasswordEncoder(passwordEncoder());
        return authProvider;
    }

    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration config) throws Exception {
        return config.getAuthenticationManager();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    // Keep these for non-security-chain filters (logging, correlation)
    @Bean
    @Order(Ordered.HIGHEST_PRECEDENCE)
    public FilterRegistrationBean<CorrelationIdFilter> correlationIdFilter() {
        FilterRegistrationBean<CorrelationIdFilter> reg = new FilterRegistrationBean<>();
        reg.setFilter(new CorrelationIdFilter());
        reg.setOrder(Ordered.HIGHEST_PRECEDENCE);
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
        // Exclude auth endpoints from API Key check
        private List<String> excludePaths = List.of(
            "/swagger-ui/**", 
            "/v3/api-docs/**", 
            "/actuator/health", 
            "/v1/auth/**",
            "/v1/brain/**", // Brain integration - no API key needed
            "/v1/dashboard/**" // Dashboard uses JWT, not API Key
        );
        private int rateLimitPerMinute = 60;

        public boolean isEnabled() { return enabled; }
        public void setEnabled(boolean enabled) { this.enabled = enabled; }
        public String getValue() { return value; }
        public void setValue(String value) { this.value = value; }
        public List<String> getExcludePaths() { return excludePaths; }
        public void setExcludePaths(List<String> excludePaths) { this.excludePaths = excludePaths; }
        public int getRateLimitPerMinute() { return rateLimitPerMinute; }
        public void setRateLimitPerMinute(int rateLimitPerMinute) { this.rateLimitPerMinute = rateLimitPerMinute; }
    }
}
