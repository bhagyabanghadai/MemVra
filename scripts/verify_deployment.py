import requests
import hmac
import hashlib
import base64
import time
import uuid
import sys
import os

# Configuration
BASE_URL = "http://localhost:8080"
API_KEY = "local-dev-api-key"
SECRET_KEY = "local-dev-change-me"

def log(msg, status="INFO"):
    print(f"[{status}] {msg}")

def fail(msg):
    log(msg, "FAIL")
    sys.exit(1)

def compute_signature(payload, secret):
    h = hmac.new(secret.encode('utf-8'), payload.encode('utf-8'), hashlib.sha256)
    return base64.b64encode(h.digest()).decode('utf-8')

def wait_for_health():
    log("Waiting for service to be healthy...")
    for i in range(30):
        try:
            r = requests.get(f"{BASE_URL}/actuator/health", timeout=2)
            if r.status_code == 200 and r.json()['status'] == 'UP':
                log("Service is UP")
                return
        except:
            pass
        time.sleep(2)
    fail("Service did not become healthy in time")

def test_happy_path():
    log("Testing Happy Path (Record & Verify)...")
    
    content = f"Test Fact {uuid.uuid4()}"
    source_id = f"test:source:{uuid.uuid4()}"
    
    payload = {
        "content": content,
        "source_type": "user_input",
        "source_id": source_id,
        "recorded_by": "verification-script"
    }
    
    headers = {"X-API-Key": API_KEY}
    
    # 1. Record Fact
    r = requests.post(f"{BASE_URL}/v1/facts", json=payload, headers=headers)
    if r.status_code != 201:
        fail(f"Failed to record fact: {r.status_code} {r.text}")
    
    resp = r.json()
    fact_id = resp['fact_id']
    signature = resp['signature']
    created_at = resp['created_at']
    
    log(f"Recorded fact: {fact_id}")
    
    # 2. Verify Signature locally
    # Payload format: externalId|content|sourceType|sourceId|recordedBy|createdAt
    # Note: createdAt from server might have different precision, need to match exactly what server signed
    # The server uses OffsetDateTime.now(ZoneOffset.UTC).withNano(0), so it should be ISO8601 without nanos
    
    # We need to reconstruct the payload exactly as the server did.
    # The server returns the fields in the response, so we use those.
    
    # Note: The server response for record might not contain all fields if DTO doesn't have them?
    # Let's check DTO. It has all fields.
    
    # Reconstruct payload
    # The server code: externalId + "|" + content + "|" + sourceType + "|" + sourceId + "|" + recordedBy + "|" + created
    # created is createdAt.withNano(0).toString()
    
    # The response `created_at` should already be the string representation.
    # However, we need to be careful about how python parses/prints it vs java.
    # But we are just concatenating strings here.
    
    # Wait, the DTO `created_at` is OffsetDateTime in Java, so it serializes to JSON string.
    # We should use the string from JSON directly.
    
    # Source Type enum value: "user_input"
    
    verify_payload = f"{fact_id}|{content}|user_input|{source_id}|verification-script|{created_at}"
    computed = compute_signature(verify_payload, SECRET_KEY)
    
    if computed != signature:
        log(f"Signature mismatch! Server: {signature}, Computed: {computed}", "ERROR")
        log(f"Payload used: {verify_payload}", "DEBUG")
        fail("Signature verification failed")
    
    log("Signature verified successfully")
    
    # 3. Get Fact
    r = requests.get(f"{BASE_URL}/v1/facts/{fact_id}", headers=headers)
    if r.status_code != 200:
        fail(f"Failed to get fact: {r.status_code}")
    
    get_resp = r.json()
    if get_resp['content'] != content:
        fail("Content mismatch in GET response")
        
    log("Fact retrieval verified")

def test_security():
    log("Testing Security Controls...")
    
    # 1. Missing API Key
    r = requests.get(f"{BASE_URL}/v1/facts/some-id")
    if r.status_code != 401:
        fail(f"Expected 401 for missing key, got {r.status_code}")
    log("Missing API Key: 401 (Pass)")
    
    # 2. Invalid API Key
    r = requests.get(f"{BASE_URL}/v1/facts/some-id", headers={"X-API-Key": "wrong-key"})
    if r.status_code != 401:
        fail(f"Expected 401 for invalid key, got {r.status_code}")
    log("Invalid API Key: 401 (Pass)")
    
    # 3. Rate Limiting (if enabled)
    # Default config has rate limit 60/min. We can try to burst it?
    # Maybe too slow to test 60 requests in a script. We'll skip strict rate limit testing 
    # unless we want to spam. Let's just verify the headers are there if we make a request?
    # The filter only adds Retry-After on failure.
    
    log("Security tests passed")

def test_validation():
    log("Testing Validation...")
    
    headers = {"X-API-Key": API_KEY}
    
    # 1. Empty Content
    payload = {
        "content": "",
        "source_type": "user_input",
        "source_id": "id",
        "recorded_by": "me"
    }
    r = requests.post(f"{BASE_URL}/v1/facts", json=payload, headers=headers)
    if r.status_code != 422: # Or 400 depending on how @Valid is handled globally
        # GlobalExceptionHandler maps MethodArgumentNotValidException to 422 usually?
        # Let's check the code.
        # FactController says: @ApiResponse(responseCode = "422", description = "Validation error")
        # So we expect 422.
        fail(f"Expected 422 for empty content, got {r.status_code}")
    log("Empty Content: 422 (Pass)")
    
    # 2. Invalid Source Type
    payload["content"] = "Valid"
    payload["source_type"] = "INVALID_TYPE"
    r = requests.post(f"{BASE_URL}/v1/facts", json=payload, headers=headers)
    if r.status_code != 400: # JSON parse error for enum
        fail(f"Expected 400 for invalid enum, got {r.status_code}")
    log("Invalid Source Type: 400 (Pass)")

    log("Validation tests passed")

def test_search():
    log("Testing Search API...")
    
    headers = {"X-API-Key": API_KEY}
    
    # 1. Create a unique fact to search for
    unique_source_id = f"search:test:{uuid.uuid4()}"
    payload = {
        "content": "Searchable Content",
        "source_type": "user_input",
        "source_id": unique_source_id,
        "recorded_by": "search-tester"
    }
    r = requests.post(f"{BASE_URL}/v1/facts", json=payload, headers=headers)
    if r.status_code != 201:
        fail(f"Failed to record searchable fact: {r.status_code}")
        
    # 2. Search by source_id
    r = requests.get(f"{BASE_URL}/v1/facts?source_id={unique_source_id}", headers=headers)
    if r.status_code != 200:
        fail(f"Search failed: {r.status_code}")
    
    # Handle paginated response
    resp_json = r.json()
    if 'content' in resp_json:
        results = resp_json['content']
    else:
        results = resp_json
        
    if len(results) != 1:
        fail(f"Expected 1 result, got {len(results)}")
    
    if results[0]['source_id'] != unique_source_id:
        fail("Search result mismatch")
        
    log("Search by source_id verified")

def test_revocation():
    log("Testing Revocation...")
    headers = {"X-API-Key": API_KEY}
    
    # 1. Record a fact
    payload = {
        "content": "To be revoked",
        "source_type": "user_input",
        "source_id": f"revoke:{uuid.uuid4()}",
        "recorded_by": "tester"
    }
    r = requests.post(f"{BASE_URL}/v1/facts", json=payload, headers=headers)
    if r.status_code != 201: fail("Failed to record fact for revocation")
    fact_id = r.json()['fact_id']
    
    # 2. Revoke it
    revoke_payload = {"reason": "Testing revocation"}
    r = requests.post(f"{BASE_URL}/v1/facts/{fact_id}/revoke", json=revoke_payload, headers=headers)
    if r.status_code != 204:
        fail(f"Revocation failed: {r.status_code}")
        
    # 3. Verify it is revoked
    r = requests.get(f"{BASE_URL}/v1/facts/{fact_id}", headers=headers)
    data = r.json()
    if not data.get('revoked'):
        fail("Fact should be revoked but isn't")
    if data.get('revocation_reason') != "Testing revocation":
        fail("Revocation reason mismatch")
        
    log("Revocation verified")

def test_batch():
    log("Testing Batch API...")
    headers = {"X-API-Key": API_KEY}
    
    batch_payload = [
        {
            "content": f"Batch fact {i}",
            "source_type": "user_input",
            "source_id": f"batch:{uuid.uuid4()}",
            "recorded_by": "tester"
        } for i in range(3)
    ]
    
    r = requests.post(f"{BASE_URL}/v1/facts/batch", json=batch_payload, headers=headers)
    if r.status_code != 201:
        fail(f"Batch recording failed: {r.status_code}")
        
    data = r.json()
    if len(data) != 3:
        fail(f"Expected 3 facts, got {len(data)}")
        
    log("Batch recording verified")

if __name__ == "__main__":
    wait_for_health()
    test_happy_path()
    test_security()
    test_validation()
    test_search()
    test_revocation()
    test_batch()
    log("ALL TESTS PASSED", "SUCCESS")
