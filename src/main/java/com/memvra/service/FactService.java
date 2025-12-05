package com.memvra.service;

import com.memvra.enums.SourceType;
import com.memvra.model.CreateFactRequest;
import com.memvra.model.FactRecord;
import com.memvra.model.FactRecordDto;
import com.memvra.repository.FactRepository;
import com.memvra.controller.BadRequestException;
import com.memvra.controller.NotFoundException;
import com.memvra.controller.ConflictException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.OffsetDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import jakarta.persistence.criteria.Predicate;

@Service
public class FactService {
    private static final Logger log = LoggerFactory.getLogger(FactService.class);

    private final FactRepository repository;
    private final CryptoService crypto;
    private final BrainService brainService;
    private final int maxContentLength;

    public FactService(FactRepository repository, CryptoService crypto, BrainService brainService,
                       @Value("${memvra.fact.max-content-length}") int maxContentLength) {
        this.repository = repository;
        this.crypto = crypto;
        this.brainService = brainService;
        this.maxContentLength = maxContentLength;
    }

    @Transactional
    public List<FactRecordDto> recordFacts(List<CreateFactRequest> requests) {
        return requests.stream().map(this::recordFact).toList();
    }

    @Transactional
    public FactRecordDto recordFact(CreateFactRequest request) {
        validateRequest(request);

        if (request.getSourceType() == SourceType.AGENT_INFERENCE) {
            log.warn("High-risk source_type detected: AGENT_INFERENCE for source_id={}", request.getSourceId());
        }

        UUID id = UUID.randomUUID();
        String externalId = "mv-" + id;
        OffsetDateTime createdAt = OffsetDateTime.now(java.time.ZoneOffset.UTC).withNano(0);

        String payload = buildPayload(externalId, request, createdAt);
        byte[] signature = crypto.sign(payload);

        FactRecord record = new FactRecord();
        record.setFactId(id);
        record.setContent(request.getContent());
        record.setSourceType(request.getSourceType());
        record.setSourceId(request.getSourceId());
        record.setRecordedBy(request.getRecordedBy());
        record.setCreatedAt(createdAt);
        record.setSignature(signature);
        record.setRevoked(false);

        try {
            record = repository.save(record);
            
            // Push to Brain asynchronously (fire and forget for now, or sync)
            try {
                Map<String, Object> factMap = new java.util.HashMap<>();
                factMap.put("content", record.getContent());
                factMap.put("fact_id", record.getFactId().toString());
                factMap.put("created_at", record.getCreatedAt().toString());
                brainService.triggerDreamCycle(List.of(factMap));
            } catch (Exception e) {
                log.error("Failed to push fact to brain: {}", e.getMessage());
                // Don't fail the transaction just because brain push failed
            }

        } catch (org.springframework.dao.DataIntegrityViolationException e) {
            throw new ConflictException("Duplicate fact detected");
        }

        return toDto(record);
    }

    public Optional<FactRecordDto> getFact(String externalId) {
        UUID id = parseExternalId(externalId);
        return repository.findById(id).map(this::toDto);
    }

    public Page<FactRecordDto> searchFacts(String sourceId, String recordedBy, SourceType sourceType, OffsetDateTime fromDate, OffsetDateTime toDate, Pageable pageable) {
        Specification<FactRecord> spec = (root, query, cb) -> {
            List<Predicate> predicates = new ArrayList<>();
            if (sourceId != null) predicates.add(cb.equal(root.get("sourceId"), sourceId));
            if (recordedBy != null) predicates.add(cb.equal(root.get("recordedBy"), recordedBy));
            if (sourceType != null) predicates.add(cb.equal(root.get("sourceType"), sourceType));
            if (fromDate != null) predicates.add(cb.greaterThanOrEqualTo(root.get("createdAt"), fromDate));
            if (toDate != null) predicates.add(cb.lessThanOrEqualTo(root.get("createdAt"), toDate));
            return cb.and(predicates.toArray(new Predicate[0]));
        };
        return repository.findAll(spec, pageable).map(this::toDto);
    }

    @Transactional
    public void revokeFact(String externalId, String reason) {
        UUID id = parseExternalId(externalId);
        FactRecord record = repository.findById(id)
                .orElseThrow(() -> new NotFoundException("Fact not found"));
        
        if (record.isRevoked()) {
            return; // Already revoked
        }

        record.setRevoked(true);
        record.setRevocationReason(reason);
        record.setRevokedAt(OffsetDateTime.now(java.time.ZoneOffset.UTC));
        repository.save(record);
    }

    private void validateRequest(CreateFactRequest request) {
        if (request.getContent() == null || request.getContent().isBlank()) {
            throw new IllegalArgumentException("content must be provided");
        }
        if (request.getContent().length() > maxContentLength) {
            throw new IllegalArgumentException("content exceeds max length of " + maxContentLength);
        }
        if (request.getSourceType() == null) {
            throw new IllegalArgumentException("source_type must be provided");
        }
        if (request.getSourceId() == null || request.getSourceId().isBlank()) {
            throw new IllegalArgumentException("source_id must be provided");
        }
        if (request.getRecordedBy() == null || request.getRecordedBy().isBlank()) {
            throw new IllegalArgumentException("recorded_by must be provided");
        }
    }

    private String buildPayload(String externalId, CreateFactRequest req, OffsetDateTime createdAt) {
        String created = createdAt.withNano(0).toString();
        return externalId + "|" +
                req.getContent() + "|" +
                req.getSourceType().toValue() + "|" +
                req.getSourceId() + "|" +
                req.getRecordedBy() + "|" +
                created;
    }

    private UUID parseExternalId(String externalId) {
        String raw = externalId.startsWith("mv-") ? externalId.substring(3) : externalId;
        try {
            return UUID.fromString(raw);
        } catch (IllegalArgumentException ex) {
            throw new BadRequestException("Invalid factId format");
        }
    }

    private FactRecordDto toDto(FactRecord record) {
        return new FactRecordDto(
            "mv-" + record.getFactId(),
            record.getContent(),
            record.getSourceType(),
            record.getSourceId(),
            record.getRecordedBy(),
            record.getCreatedAt(),
            crypto.toBase64(record.getSignature()),
            record.isRevoked(),
            record.getRevocationReason(),
            record.getRevokedAt()
        );
    }
}