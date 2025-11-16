package com.compyle.memvra.controller;

import com.compyle.memvra.model.CreateFactRequest;
import com.compyle.memvra.model.FactRecordDto;
import com.compyle.memvra.service.FactService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@RestController
@RequestMapping("/v1/facts")
public class FactController {

    private final FactService factService;

    public FactController(FactService factService) {
        this.factService = factService;
    }

    @PostMapping
    public ResponseEntity<FactRecordDto> record(@Valid @RequestBody CreateFactRequest request) {
        FactRecordDto dto = factService.recordFact(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(dto);
    }

    @GetMapping("/{factId}")
    public ResponseEntity<?> get(@PathVariable String factId) {
        Optional<FactRecordDto> dto = factService.getFact(factId);
        return dto.<ResponseEntity<?>>map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(new com.compyle.memvra.model.ErrorResponse("NOT_FOUND", "Fact not found", null)));
    }

    // GlobalExceptionHandler covers validation and bad JSON; keeping controller lean
}