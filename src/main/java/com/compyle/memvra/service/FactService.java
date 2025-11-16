package com.compyle.memvra.service;

import com.compyle.memvra.enums.SourceType;
import com.compyle.memvra.model.CreateFactRequest;
import com.compyle.memvra.model.FactRecord;
import com.compyle.memvra.model.FactRecordDto;
import com.compyle.memvra.repository.FactRepository;
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
                       @Value("${compyle.fact.max-content-length}") int maxContentLength) {
        this.repository = repository;
        this.crypto = crypto;
        this.maxContentLength = maxContentLength;
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

        FactRecord rec = new FactRecord();
        rec.setFactId(id);
        rec.setContent(request.getContent());
        rec.setSourceType(request.getSourceType());
        rec.setSourceId(request.getSourceId());
        rec.setRecordedBy(request.getRecordedBy());
        rec.setCreatedAt(createdAt);
        rec.setSignature(signature);
        repository.save(rec);

        return new FactRecordDto(
                externalId,
                rec.getContent(),
                rec.getSourceType(),
                rec.getSourceId(),
                rec.getRecordedBy(),
                rec.getCreatedAt(),
                crypto.toBase64(signature)
        );
    }

    public Optional<FactRecordDto> getFact(String externalId) {
        UUID id = parseExternalId(externalId);
        return repository.findById(id).map(rec -> new FactRecordDto(
                "mv-" + rec.getFactId(),
                rec.getContent(),
                rec.getSourceType(),
                rec.getSourceId(),
                rec.getRecordedBy(),
                rec.getCreatedAt(),
                crypto.toBase64(rec.getSignature())
        ));
    }

    private void validateRequest(CreateFactRequest request) {
        if (request.getContent() == null || request.getContent().trim().isEmpty()) {
            throw new IllegalArgumentException("content must be non-empty");
        }
        if (request.getContent().length() > maxContentLength) {
            throw new IllegalArgumentException("content exceeds max length " + maxContentLength);
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
        return UUID.fromString(raw);
    }
}