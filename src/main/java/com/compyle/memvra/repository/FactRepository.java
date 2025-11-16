package com.compyle.memvra.repository;

import com.compyle.memvra.model.FactRecord;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.UUID;

public interface FactRepository extends JpaRepository<FactRecord, UUID> {
}