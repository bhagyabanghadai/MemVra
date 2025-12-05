# verify_all_datasets.ps1
# Comprehensive verification of MemVra Brain with all generated datasets

$baseUrl = "http://localhost:8000"
$datasets = @("small", "medium", "large", "extra_large", "full", "massive")

function Test-Dataset {
    param (
        [string]$Size
    )
    
    $filePath = "memvra-brain/data/test_batch_$Size.json"
    if (-not (Test-Path $filePath)) {
        Write-Host "⚠️ Dataset $Size not found at $filePath" -ForegroundColor Red
        return
    }

    Write-Host "`nTesting Dataset: $Size" -ForegroundColor Cyan
    $content = Get-Content $filePath | ConvertFrom-Json
    $count = $content.facts.Count
    Write-Host "  - Input Memories: $count" -ForegroundColor Gray

    $startTime = Get-Date
    try {
        $jsonPayload = $content | ConvertTo-Json -Depth 10
        $response = Invoke-RestMethod -Uri "$baseUrl/v1/intuitive/dream" -Method POST -Body $jsonPayload -ContentType "application/json"
        $duration = (Get-Date) - $startTime

        Write-Host "  - Status: ✅ Success" -ForegroundColor Green
        Write-Host "  - Time: $($duration.TotalMilliseconds) ms" -ForegroundColor Gray
        Write-Host "  - Summary: $($response.summary)" -ForegroundColor Yellow
        Write-Host "  - Sentiment: $($response.sentiment)" -ForegroundColor Yellow
        Write-Host "  - Patterns Detected: $($response.patterns.Count)" -ForegroundColor Yellow
        return $true
    }
    catch {
        Write-Host "  - Status: ❌ Failed" -ForegroundColor Red
        Write-Host "  - Error: $_" -ForegroundColor Red
        return $false
    }
}

function Test-Recall {
    param (
        [string]$Query,
        [string]$ExpectedContext
    )

    Write-Host "`nTesting Recall: '$Query'" -ForegroundColor Cyan
    try {
        $response = Invoke-RestMethod -Uri "$baseUrl/v1/logical/recall?query=$Query" -Method POST
        
        if ($response.matches) {
            $matchCount = $response.matches.Count
            Write-Host "  - Found: $matchCount memories" -ForegroundColor Green
            $firstMatch = $response.matches[0].content
            Write-Host "  - Top Result: $firstMatch" -ForegroundColor Gray
            
            if ($firstMatch -match $ExpectedContext) {
                 Write-Host "  - Context Verification: ✅ Verified ('$ExpectedContext' found)" -ForegroundColor Green
            } else {
                 Write-Host "  - Context Verification: ⚠️ Potential Mismatch (Expected '$ExpectedContext')" -ForegroundColor Yellow
            }
        } else {
            Write-Host "  - Found: 0 memories" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "  - Recall Failed: $_" -ForegroundColor Red
    }
}

Write-Host "=========================================" -ForegroundColor Magenta
Write-Host "  MEMVRA BRAIN - COMPREHENSIVE TEST" -ForegroundColor Magenta
Write-Host "========================================="

# 1. Check Initial Status
$status = Invoke-RestMethod -Uri "$baseUrl/"
Write-Host "`nInitial Brain Status:" -ForegroundColor Cyan
Write-Host "  - Memories Stored: $($status.memories_stored)" -ForegroundColor Green

# 2. Test All Datasets
foreach ($ds in $datasets) {
    Test-Dataset -Size $ds
    Start-Sleep -Milliseconds 500
}

# 3. Verify Interactions (Recall)
Write-Host "`n=========================================" -ForegroundColor Magenta
Write-Host "  VERIFYING INTERACTIONS & RECALL" -ForegroundColor Magenta
Write-Host "========================================="

# Test specific concepts we know exist in the synthetic data
Test-Recall -Query "authentication" -ExpectedContext "authentication"
Test-Recall -Query "bug" -ExpectedContext "bug"
Test-Recall -Query "family" -ExpectedContext "family"
Test-Recall -Query "optimization" -ExpectedContext "optimization"

# 4. Final Status
$finalStatus = Invoke-RestMethod -Uri "$baseUrl/"
Write-Host "`n=========================================" -ForegroundColor Magenta
Write-Host "  FINAL STATUS" -ForegroundColor Magenta
Write-Host "========================================="
Write-Host "  - Total Memories Stored: $($finalStatus.memories_stored)" -ForegroundColor Green
Write-Host "  - Brain Health: $($finalStatus.status)" -ForegroundColor Green
