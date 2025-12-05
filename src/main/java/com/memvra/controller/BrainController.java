package com.memvra.controller;

import com.memvra.service.BrainService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/v1/brain")
public class BrainController {

    private final BrainService brainService;

    public BrainController(BrainService brainService) {
        this.brainService = brainService;
    }

    @PostMapping("/recall")
    public ResponseEntity<String> recallFact(@RequestParam String query) {
        String result = brainService.recallLogicalFact(query);
        return ResponseEntity.ok(result);
    }

    @GetMapping("/status")
    public ResponseEntity<Map<String, String>> getBrainStatus() {
        return ResponseEntity.ok(Map.of(
            "status", "Brain integration active",
            "logicalBrain", "BabyDragon (Recall)",
            "intuitiveBrain", "TinyRecursive (Dream)"
        ));
    }
}
