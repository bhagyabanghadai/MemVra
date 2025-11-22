package com.memvra.repository;

import com.memvra.model.FactRecord;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import java.util.UUID;

public interface FactRepository extends JpaRepository<FactRecord, UUID>, JpaSpecificationExecutor<FactRecord> {
    boolean existsByContentAndSourceIdAndRecordedBy(String content, String sourceId, String recordedBy);
}