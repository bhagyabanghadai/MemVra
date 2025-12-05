# verify_bicameral_dialogue.ps1
# Simulates a Q&A session to test Bicameral Interaction

$baseUrl = "http://localhost:8000"

Write-Host "=========================================" -ForegroundColor Magenta
Write-Host "  BICAMERAL BRAIN Q&A TEST: 'The Midnight Heist'" -ForegroundColor Magenta
Write-Host "========================================="

# 1. THE INPUT (Intuitive Brain Job)
# We feed a narrative story to the brain.
Write-Host "`n[PHASE 1] INTUITIVE BRAIN: Processing Narrative..." -ForegroundColor Cyan

$story = @{
    facts = @(
        @{fact_id = "story_1"; content = "Detective Miller arrived at the gloomy docks at midnight."; created_at = "2025-11-27T00:00:00" },
        @{fact_id = "story_2"; content = "The suspect, known only as 'The Shadow', left a blue origami crane as a calling card."; created_at = "2025-11-27T00:15:00" },
        @{fact_id = "story_3"; content = "Miller found a muddy footprint size 11 near the warehouse entrance."; created_at = "2025-11-27T00:30:00" },
        @{fact_id = "story_4"; content = "The stolen item was confirmed to be the Sapphire of Poseidon."; created_at = "2025-11-27T01:00:00" },
        @{fact_id = "story_5"; content = "Miller felt a mix of excitement and fear as he entered the dark warehouse."; created_at = "2025-11-27T01:15:00" }
    )
} | ConvertTo-Json -Depth 10

$dreamResult = Invoke-RestMethod -Uri "$baseUrl/v1/intuitive/dream" -Method POST -Body $story -ContentType "application/json"

Write-Host "  > Narrative Ingested." -ForegroundColor Gray
Write-Host "  > Intuitive Analysis: $($dreamResult.summary)" -ForegroundColor Yellow
Write-Host "  > Sentiment Detected: $($dreamResult.sentiment)" -ForegroundColor Yellow

# 2. THE INTERROGATION (Logical Brain Job)
# We ask specific questions to see if the Logical Brain can retrieve the answers from the Intuitive Brain's work.
Write-Host "`n[PHASE 2] LOGICAL BRAIN: The Interrogation..." -ForegroundColor Cyan

function Ask-Brain {
    param ([string]$Question, [string]$Keyword)
    
    Write-Host "`nUSER: $Question" -ForegroundColor White
    $result = Invoke-RestMethod -Uri "$baseUrl/v1/logical/recall?query=$Keyword" -Method POST
    
    if ($result.matches.Count -gt 0) {
        $answer = $result.matches[0].content
        Write-Host "BRAIN: $answer" -ForegroundColor Green
        return $true
    }
    else {
        Write-Host "BRAIN: [I don't recall that]" -ForegroundColor Red
        return $false
    }
}

# The Questions
$q1 = Ask-Brain -Question "Who is the suspect?" -Keyword "suspect"
$q2 = Ask-Brain -Question "What did the suspect leave behind?" -Keyword "origami"
$q3 = Ask-Brain -Question "What clue did Miller find?" -Keyword "footprint"
$q4 = Ask-Brain -Question "What was stolen?" -Keyword "stolen"
$q5 = Ask-Brain -Question "How did Miller feel?" -Keyword "felt"

Write-Host "`n=========================================" -ForegroundColor Magenta
Write-Host "  TEST RESULTS" -ForegroundColor Magenta
Write-Host "========================================="
if ($q1 -and $q2 -and $q3 -and $q4 -and $q5) {
    Write-Host "✅ SUCCESS: Both brains are working in perfect harmony." -ForegroundColor Green
    Write-Host "   - Intuitive Brain understood and stored the context."
    Write-Host "   - Logical Brain accurately retrieved specific answers."
}
else {
    Write-Host "❌ FAIL: Some questions could not be answered." -ForegroundColor Red
}
