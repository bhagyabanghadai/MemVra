package com.compyle.memvra.config;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Contact;
import io.swagger.v3.oas.annotations.info.Info;
import io.swagger.v3.oas.annotations.servers.Server;
import io.swagger.v3.oas.annotations.security.SecurityScheme;
import io.swagger.v3.oas.annotations.enums.SecuritySchemeType;
import io.swagger.v3.oas.annotations.enums.SecuritySchemeIn;
// OpenAPI security scheme can be added later if needed.
import org.springframework.context.annotation.Configuration;

@Configuration
@SecurityScheme(
        name = "ApiKeyAuth",
        type = SecuritySchemeType.APIKEY,
        in = SecuritySchemeIn.HEADER,
        paramName = "X-API-Key"
)
@OpenAPIDefinition(
        info = @Info(
                title = "MemVra Truth Ledger API",
                version = "v0.1.0",
                description = "Record and retrieve signed facts with provenance",
                contact = @Contact(name = "MemVra", url = "https://example.com")
        ),
        servers = {
                @Server(url = "http://localhost:8080", description = "Local" )
        }
)
public class OpenApiConfig {
    // Default Springdoc configuration is sufficient for MVP.
}