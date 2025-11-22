package com.memvra.controller;

import com.memvra.model.CreateFactRequest;
import com.memvra.model.FactRecordDto;
import com.memvra.service.FactService;
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
            content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.memvra.model.ErrorResponse.class))),
            @ApiResponse(responseCode = "422", description = "Validation error",
            content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.memvra.model.ErrorResponse.class))),
            @ApiResponse(responseCode = "409", description = "Conflict (duplicate fact)",
            content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.memvra.model.ErrorResponse.class)))
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
            content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.memvra.model.ErrorResponse.class)))
    })
    public ResponseEntity<?> get(@PathVariable String factId) {
        Optional<FactRecordDto> dto = factService.getFact(factId);
        return dto.<ResponseEntity<?>>map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.status(HttpStatus.NOT_FOUND)
                .body(new com.memvra.model.ErrorResponse("NOT_FOUND", "Fact not found", null)));
    }

    @GetMapping
    @SecurityRequirement(name = "ApiKeyAuth")
    @Operation(summary = "Search facts", description = "Search facts by source_id, recorded_by, or source_type.")
    @ApiResponse(responseCode = "200", description = "OK",
            content = @Content(mediaType = "application/json", schema = @Schema(implementation = FactRecordDto.class)))
    public ResponseEntity<org.springframework.data.domain.Page<FactRecordDto>> search(
            @RequestParam(required = false, name = "source_id") String sourceId,
            @RequestParam(required = false, name = "recorded_by") String recordedBy,
            @RequestParam(required = false, name = "source_type") com.memvra.enums.SourceType sourceType,
            @RequestParam(required = false, name = "from_date") @org.springframework.format.annotation.DateTimeFormat(iso = org.springframework.format.annotation.DateTimeFormat.ISO.DATE_TIME) java.time.OffsetDateTime fromDate,
            @RequestParam(required = false, name = "to_date") @org.springframework.format.annotation.DateTimeFormat(iso = org.springframework.format.annotation.DateTimeFormat.ISO.DATE_TIME) java.time.OffsetDateTime toDate,
            @org.springdoc.core.annotations.ParameterObject org.springframework.data.domain.Pageable pageable) {
        return ResponseEntity.ok(factService.searchFacts(sourceId, recordedBy, sourceType, fromDate, toDate, pageable));
    }

    @PostMapping("/{factId}/revoke")
    @SecurityRequirement(name = "ApiKeyAuth")
    @Operation(summary = "Revoke a fact", description = "Mark a fact as revoked without deleting it.")
    @ApiResponses({
            @ApiResponse(responseCode = "204", description = "Revoked successfully"),
            @ApiResponse(responseCode = "404", description = "Fact not found")
    })
    public ResponseEntity<Void> revoke(
            @PathVariable String factId,
            @RequestBody(required = false) java.util.Map<String, String> body) {
        String reason = body != null ? body.getOrDefault("reason", "No reason provided") : "No reason provided";
        factService.revokeFact(factId, reason);
        return ResponseEntity.noContent().build();
    }

    @PostMapping("/batch")
    @SecurityRequirement(name = "ApiKeyAuth")
    @Operation(summary = "Record multiple facts", description = "Creates multiple signed facts in a single transaction.")
    @ApiResponses({
            @ApiResponse(responseCode = "201", description = "Created",
                    content = @Content(mediaType = "application/json", schema = @Schema(implementation = FactRecordDto.class))),
            @ApiResponse(responseCode = "400", description = "Bad request"),
            @ApiResponse(responseCode = "422", description = "Validation error")
    })
    public ResponseEntity<java.util.List<FactRecordDto>> recordBatch(@Valid @RequestBody java.util.List<CreateFactRequest> requests) {
        if (requests.size() > 50) {
            throw new com.memvra.controller.BadRequestException("Batch size limit exceeded (max 50)");
        }
        java.util.List<FactRecordDto> dtos = factService.recordFacts(requests);
        return ResponseEntity.status(HttpStatus.CREATED).body(dtos);
    }

    // GlobalExceptionHandler covers validation and bad JSON; keeping controller lean
}