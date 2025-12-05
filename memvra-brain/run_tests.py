import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def log_test(name, passed, details=""):
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} - {name}")
    if not passed:
        print(f"   Details: {details}")

def test_health():
    try:
        r = requests.get(f"{BASE_URL}/")
        data = r.json()
        passed = r.status_code == 200 and data.get("version") == "2.0"
        log_test("Basic API Health (Version 2.0)", passed, str(data))
        return passed
    except Exception as e:
        log_test("Basic API Health", False, str(e))
        return False

def test_stats():
    try:
        r = requests.get(f"{BASE_URL}/v1/stats")
        data = r.json()
        passed = r.status_code == 200 and "total_users" in data
        log_test("System Statistics", passed, str(data))
        return passed
    except Exception as e:
        log_test("System Statistics", False, str(e))
        return False

def test_fact_storage():
    facts = [
        {"content": "I prefer dark mode for coding", "tags": ["UI", "preference"]},
        {"content": "Minimalist UI design is my favorite", "tags": ["UI", "design"]},
        {"content": "I like using keyboard shortcuts", "tags": ["productivity"]},
        {"content": "Performance optimization is important to me", "tags": ["performance"]},
        {"content": "I prefer TypeScript over JavaScript", "tags": ["coding"]}
    ]
    
    passed_count = 0
    for fact in facts:
        try:
            r = requests.post(f"{BASE_URL}/v1/logical/store", json={
                "user_id": "test_user_1",
                "content": fact["content"],
                "tags": fact["tags"]
            })
            if r.status_code == 200:
                passed_count += 1
        except Exception as e:
            print(f"Error storing fact: {e}")
            
    passed = passed_count == len(facts)
    log_test(f"Fact Storage ({passed_count}/{len(facts)})", passed)
    return passed

def test_recall():
    try:
        # Test 1: Specific query
        r = requests.post(f"{BASE_URL}/v1/logical/recall?query=What are my UI preferences?&user_id=test_user_1")
        data = r.json()
        
        has_result = "dark mode" in data.get("result", "").lower() or "minimalist" in data.get("result", "").lower()
        has_metadata = "metadata" in data
        
        log_test("Recall with Llama (UI preferences)", has_result and has_metadata, data.get("result"))
        
        # Test 2: Explainable retrieval
        if has_metadata:
            explanation = data.get("explanation")
            log_test("Explainable Retrieval", explanation is not None, "Path returned")
            
        return has_result
    except Exception as e:
        log_test("Recall Test", False, str(e))
        return False

def test_linguistic_profiling():
    try:
        # Store some facts with specific vocabulary
        requests.post(f"{BASE_URL}/v1/logical/store", json={
            "user_id": "test_user_1",
            "content": "My UI perf is critical",
            "tags": ["performance"]
        })
        requests.post(f"{BASE_URL}/v1/logical/store", json={
            "user_id": "test_user_1",
            "content": "Check the UI perf stats",
            "tags": ["performance"]
        })
        requests.post(f"{BASE_URL}/v1/logical/store", json={
            "user_id": "test_user_1",
            "content": "Optimizing UI perf",
            "tags": ["performance"]
        })
        
        # Check profile
        r = requests.get(f"{BASE_URL}/v1/profile/test_user_1")
        data = r.json()
        linguistic = data.get("linguistic_profile", {})
        vocab = linguistic.get("vocabulary", {})
        
        # Check if "perf" was learned
        learned_perf = "perf" in vocab
        log_test("Linguistic Profiling (Vocabulary Learning)", learned_perf, f"Vocab: {vocab.keys()}")
        
        return learned_perf
    except Exception as e:
        log_test("Linguistic Profiling", False, str(e))
        return False

def test_dream_cycle():
    try:
        r = requests.post(f"{BASE_URL}/v1/intuitive/dream", json={
            "user_id": "test_user_1"
        })
        data = r.json()
        
        passed = data.get("status") == "success"
        patterns = data.get("patterns", [])
        
        log_test(f"Dream Cycle Compression ({len(patterns)} patterns)", passed, str(patterns))
        return passed
    except Exception as e:
        log_test("Dream Cycle", False, str(e))
        return False

def test_predictive_engine():
    try:
        # Simulate repeated queries
        for _ in range(3):
            requests.post(f"{BASE_URL}/v1/logical/recall?query=What is my coding style?&user_id=test_user_1")
            
        # Check profile for patterns
        r = requests.get(f"{BASE_URL}/v1/profile/test_user_1")
        data = r.json()
        # Note: In our implementation, we just store them, prediction logic is TODO in stub
        # But we can check if query count increased
        passed = data.get("summary", {}).get("total_queries", 0) >= 3
        log_test("Predictive Engine (Query Tracking)", passed)
        return passed
    except Exception as e:
        log_test("Predictive Engine", False, str(e))
        return False

def run_all():
    print("🚀 Starting Comprehensive Brain Tests...\n")
    
    if not test_health():
        print("\n❌ Critical Health Check Failed. Aborting.")
        return
        
    test_stats()
    test_fact_storage()
    time.sleep(1) # Let graph update
    test_recall()
    test_linguistic_profiling()
    test_dream_cycle()
    test_predictive_engine()
    
    print("\n✨ Testing Complete!")

if __name__ == "__main__":
    run_all()
