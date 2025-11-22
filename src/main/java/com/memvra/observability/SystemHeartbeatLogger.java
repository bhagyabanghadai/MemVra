package com.memvra.observability;

import com.memvra.repository.FactRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.lang.management.ManagementFactory;
import java.time.Duration;

@Component
public class SystemHeartbeatLogger {
    private static final Logger log = LoggerFactory.getLogger(SystemHeartbeatLogger.class);

    private final FactRepository repo;
    private final boolean enabled;

    public SystemHeartbeatLogger(FactRepository repo,
                                 @Value("${memvra.logging.heartbeat-enabled:true}") boolean enabled) {
        this.repo = repo;
        this.enabled = enabled;
    }

    // Logs every 5 minutes by default; can be tuned via property if needed
    @Scheduled(fixedRateString = "${memvra.logging.heartbeat-ms:300000}")
    public void heartbeat() {
        if (!enabled) return;
        long uptimeMs = ManagementFactory.getRuntimeMXBean().getUptime();
        long minutes = Duration.ofMillis(uptimeMs).toMinutes();
        long count = 0;
        try {
            count = repo.count();
        } catch (Exception e) {
            log.warn("Heartbeat: failed to query fact count: {}", e.getMessage());
        }
        log.info("Heartbeat: uptime_min={} facts_total={} status=OK", minutes, count);
    }
}