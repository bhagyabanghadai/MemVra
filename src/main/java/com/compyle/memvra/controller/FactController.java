package com.compyle.memvra.controller;

import com.compyle.memvra.model.CreateFactRequest;
import com.compyle.memvra.model.FactRecordDto;
import com.compyle.memvra.service.FactService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;

import java.util.Optional;

@RestController
@RequestMapping("/v1/facts")
public class FactController {

    private final FactService factService;

    public FactController(FactService factService) {
        this.factService = factService;
    }

    @PostMapping
    @SecurityRequirement(name = "ApiKeyAuth")
    @Operation(summary = "Record a fact", description = "Creates a signed fact with provenance and returns the record.")
    @ApiResponses({
            @ApiResponse(responseCode = "201", description = "Created",
                    content = @Content(mediaType = "application/json", schema = @Schema(implementation = FactRecordDto.class))),
            @ApiResponse(responseCode = "400", description = "Bad request (malformed JSON)",
                    content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.compyle.memvra.model.ErrorResponse.class))),
            @ApiResponse(responseCode = "422", description = "Validation error",
                    content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.compyle.memvra.model.ErrorResponse.class)))
    })
    public ResponseEntity<FactRecordDto> record(@Valid @RequestBody CreateFactRequest request) {
        FactRecordDto dto = factService.recordFact(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(dto);
    }

    @GetMapping("/{factId}")
    @SecurityRequirement(name = "ApiKeyAuth")
    @Operation(summary = "Get a fact", description = "Fetches a previously recorded fact by its external ID (mv-UUID).")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "OK",
                    content = @Content(mediaType = "application/json", schema = @Schema(implementation = FactRecordDto.class))),
            @ApiResponse(responseCode = "404", description = "Not found",
                    content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.compyle.memvra.model.ErrorResponse.class)))
    })
    public ResponseEntity<?> get(@PathVariable String factId) {
        Optional<FactRecordDto> dto = factService.getFact(factId);
        return dto.<ResponseEntity<?>>map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(new com.compyle.memvra.model.ErrorResponse("NOT_FOUND", "Fact not found", null)));
    }

    // GlobalExceptionHandler covers validation and bad JSON; keeping controller lean
}