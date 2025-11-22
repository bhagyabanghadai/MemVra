package com.memvra.service;

import com.memvra.enums.SourceType;
import com.memvra.model.CreateFactRequest;
import com.memvra.model.FactRecord;
import com.memvra.model.FactRecordDto;
import com.memvra.repository.FactRepository;
import org.springframework.dao.DataIntegrityViolationException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.OffsetDateTime;
import java.util.Optional;
import java.util.UUID;

@Service
public class FactService {
    private static final Logger log = LoggerFactory.getLogger(FactService.class);

    private final FactRepository repository;
    private final CryptoService crypto;
    private final int maxContentLength;

    public FactService(FactRepository repository, CryptoService crypto,
                       @Value("${memvra.fact.max-content-length}") int maxContentLength) {
        this.repository = repository;
        this.crypto = crypto;
        this.maxContentLength = maxContentLength;
    }

    @Transactional
    public java.util.List<FactRecordDto> recordFacts(java.util.List<CreateFactRequest> requests) {
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
        throw new com.memvra.controller.BadRequestException("Invalid factId format");
        }
    }
}