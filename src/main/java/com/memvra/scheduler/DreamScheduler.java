package com.memvra.scheduler;

import com.memvra.service.BrainService;
import com.memvra.repository.FactRepository;
import com.memvra.model.FactRecord;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Component
public class DreamScheduler {

    private static final Logger log = LoggerFactory.getLogger(DreamScheduler.class);

    private final BrainService brainService;
    private final FactRepository factRepository;

    public DreamScheduler(BrainService brainService, FactRepository factRepository) {
        this.brainService = brainService;
        this.factRepository = factRepository;
    }

    @org.springframework.context.event.EventListener(org.springframework.boot.context.event.ApplicationReadyEvent.class)
    public void onStartup() {
        runDreamCycle();
    }

    // Run every hour (3600000 ms)
    @Scheduled(fixedRate = 3600000)
    public void runDreamCycle() {
        log.info("Starting Dream Cycle: Consolidating memories...");

        // Fetch recent facts (placeholder logic - in real app, fetch un-consolidated facts)
        List<FactRecord> recentFacts = factRepository.findAll(); 
        
        if (recentFacts.isEmpty()) {
            log.info("No new memories to consolidate. Sleeping.");
            return;
        }

        // Convert to format expected by Brain
        List<Map<String, Object>> factData = recentFacts.stream()
            .limit(10) // Limit for demo
            .map(f -> {
                Map<String, Object> map = new java.util.HashMap<>();
                map.put("content", f.getContent());
                map.put("fact_id", f.getFactId().toString());
                map.put("created_at", f.getCreatedAt().toString());
                return map;
            })
            .collect(Collectors.toList());

        // Trigger Dream
        Map<String, Object> insight = brainService.triggerDreamCycle(factData);
        
        log.info("Dream Cycle Complete. Insight: {}", insight);
        
        // In a real implementation, we would save this insight as a new FactRecord
    }
}
