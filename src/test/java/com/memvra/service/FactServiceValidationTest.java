package com.memvra.service;

import com.memvra.enums.SourceType;
import com.memvra.model.CreateFactRequest;
import com.memvra.repository.FactRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.dao.DataIntegrityViolationException;

import static org.junit.jupiter.api.Assertions.*;

public class FactServiceValidationTest {

    private FactRepository repo;
    private CryptoService crypto;
    private FactService service;

    @BeforeEach
    void setup() {
        repo = Mockito.mock(FactRepository.class);
        crypto = new CryptoService("unit-test-secret");
        service = new FactService(repo, crypto, 1000);
    }

    @Test
    void emptyContentThrows() {
        CreateFactRequest req = new CreateFactRequest();
        req.setContent("   ");
        req.setSourceType(SourceType.USER_INPUT);
        req.setSourceId("s");
        req.setRecordedBy("a");
        assertThrows(IllegalArgumentException.class, () -> service.recordFact(req));
    }

    @Test
    void missingSourceTypeThrows() {
        CreateFactRequest req = new CreateFactRequest();
        req.setContent("ok");
        req.setSourceType(null);
        req.setSourceId("s");
        req.setRecordedBy("a");
        assertThrows(IllegalArgumentException.class, () -> service.recordFact(req));
    }

    @Test
    void missingSourceIdThrows() {
        CreateFactRequest req = new CreateFactRequest();
        req.setContent("ok");
        req.setSourceType(SourceType.USER_INPUT);
        req.setSourceId(" ");
        req.setRecordedBy("a");
        assertThrows(IllegalArgumentException.class, () -> service.recordFact(req));
    }

    @Test
    void missingRecordedByThrows() {
        CreateFactRequest req = new CreateFactRequest();
        req.setContent("ok");
        req.setSourceType(SourceType.USER_INPUT);
        req.setSourceId("s");
        req.setRecordedBy(" ");
        assertThrows(IllegalArgumentException.class, () -> service.recordFact(req));
    }

    @Test
    void duplicateFactThrowsConflict() {
        CreateFactRequest req = new CreateFactRequest();
        req.setContent("same");
        req.setSourceType(SourceType.USER_INPUT);
        req.setSourceId("src-1");
        req.setRecordedBy("agent-1");

        Mockito.doThrow(new DataIntegrityViolationException("duplicate"))
                .when(repo).saveAndFlush(Mockito.any());

        assertThrows(com.memvra.controller.ConflictException.class, () -> service.recordFact(req));
    }
}