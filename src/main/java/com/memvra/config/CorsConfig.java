package com.memvra.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

@Configuration
public class CorsConfig implements WebMvcConfigurer {

    @Value("${memvra.cors.allowed-origins:}")
    private String allowedOriginsCsv;

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        List<String> origins = parseOrigins(allowedOriginsCsv);
        if (!origins.isEmpty()) {
            registry.addMapping("/v1/**")
                    .allowedOrigins(origins.toArray(new String[0]))
                    .allowedMethods("GET", "POST")
                    .allowedHeaders("Content-Type", "X-API-Key", "X-Correlation-Id")
                    .exposedHeaders("X-Correlation-Id")
                    .allowCredentials(false)
                    .maxAge(3600);
            // Allow Swagger for local development when a front-end origin is specified
            registry.addMapping("/v3/api-docs/**")
                    .allowedOrigins(origins.toArray(new String[0]))
                    .allowedMethods("GET")
                    .allowedHeaders("*")
                    .allowCredentials(false)
                    .maxAge(3600);
            registry.addMapping("/swagger-ui/**")
                    .allowedOrigins(origins.toArray(new String[0]))
                    .allowedMethods("GET")
                    .allowedHeaders("*")
                    .allowCredentials(false)
                    .maxAge(3600);
        }
    }

    private static List<String> parseOrigins(String csv) {
        if (csv == null || csv.isBlank()) {
            return List.of();
        }
        return Arrays.stream(csv.split(","))
                .map(String::trim)
                .filter(s -> !s.isBlank())
                .collect(Collectors.toList());
    }
}