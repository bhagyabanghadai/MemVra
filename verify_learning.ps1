# verify_learning_and_interaction.ps1
# Demonstrates Self-Learning (Emergent Themes) and Bicameral Interaction

$baseUrl = "http://localhost:8000"

Write-Host "=========================================" -ForegroundColor Magenta
Write-Host "  TESTING SELF-LEARNING & INTERACTION" -ForegroundColor Magenta
Write-Host "========================================="

# 1. BASELINE: What does the brain know now?
Write-Host "`n1. CHECKING CURRENT KNOWLEDGE..." -ForegroundColor Cyan
$status = Invoke-RestMethod -Uri "$baseUrl/"
Write-Host "   Memories Stored: $($status.memories_stored)" -ForegroundColor Yellow

# 2. TEACHING: Feed a completely NEW topic (e.g., "Gardening")
# The brain has NO pre-programmed knowledge of gardening.
Write-Host "`n2. LEARNING PHASE: Feeding new 'Gardening' topic..." -ForegroundColor Cyan
$newTopic = @{
    facts = @(
        @{fact_id = "new_1"; content = "Started a new vegetable garden in the backyard"; created_at = "2025-11-26T09:00:00" },
        @{fact_id = "new_2"; content = "Planted tomatoes and peppers in the garden"; created_at = "2025-11-26T10:00:00" },
        @{fact_id = "new_3"; content = "The garden soil needs more compost for the tomatoes"; created_at = "2025-11-26T11:00:00" },
        @{fact_id = "new_4"; content = "Watered the garden early in the morning"; created_at = "2025-11-26T12:00:00" },
        @{fact_id = "new_5"; content = "Tomatoes are growing fast in the new garden"; created_at = "2025-11-26T13:00:00" }
    )
} | ConvertTo-Json -Depth 10

$dreamResult = Invoke-RestMethod -Uri "$baseUrl/v1/intuitive/dream" -Method POST -Body $newTopic -ContentType "application/json"

# 3. VERIFY SELF-LEARNING (Did it detect the new themes?)
Write-Host "`n3. VERIFYING SELF-LEARNING (Intuitive Brain)..." -ForegroundColor Cyan
Write-Host "   Summary: $($dreamResult.summary)" -ForegroundColor Green
Write-Host "   Key Insights: $($dreamResult.key_insights -join ', ')" -ForegroundColor Green

if ($dreamResult.summary -match "garden" -or $dreamResult.summary -match "tomatoes") {
    Write-Host "   ✅ SUCCESS: Brain automatically learned 'Garden'/'Tomatoes' as a new theme!" -ForegroundColor Green
}
else {
    Write-Host "   ❌ FAIL: Brain did not detect the new theme." -ForegroundColor Red
}

# 4. VERIFY BICAMERAL INTERACTION (Can Logical Brain access Intuitive Brain's work?)
Write-Host "`n4. VERIFYING BICAMERAL INTERACTION..." -ForegroundColor Cyan
Write-Host "   Action: Logical Brain querying for 'tomatoes'..." -ForegroundColor Gray

$recallResult = Invoke-RestMethod -Uri "$baseUrl/v1/logical/recall?query=tomatoes" -Method POST

if ($recallResult.matches.Count -gt 0) {
    Write-Host "   ✅ SUCCESS: Logical Brain retrieved $($recallResult.matches.Count) memories about 'tomatoes'." -ForegroundColor Green
    Write-Host "   Top Match: $($recallResult.matches[0].content)" -ForegroundColor Gray
    Write-Host "`n   CONCLUSION: The Intuitive Brain (Dream) successfully consolidated the info,"
    Write-Host "   and the Logical Brain (Recall) successfully accessed it."
    Write-Host "   The two systems are interacting perfectly via the shared memory store."
}
else {
    Write-Host "   ❌ FAIL: Logical Brain could not find the memories." -ForegroundColor Red
}
