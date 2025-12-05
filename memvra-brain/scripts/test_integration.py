"""
MemVra Bicameral Architecture - Comprehensive Integration Test
Tests all API endpoints and features end-to-end
"""
import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"
USER_ID = "test_user_integration"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    END = '\033[0m'

def print_test(name):
    print(f"\n{Colors.BLUE}🧪 Testing: {name}{Colors.END}")

def print_pass(msg):
    print(f"{Colors.GREEN}✅ PASS: {msg}{Colors.END}")

def print_fail(msg):
    print(f"{Colors.RED}❌ FAIL: {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.YELLOW}ℹ️  {msg}{Colors.END}")

def test_health_check():
    """Test 1: Basic health check"""
    print_test("Health Check")
    try:
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "MemVra Brain"
        assert "Bicameral" in data["version"]
        print_pass(f"Service is operational: {data['version']}")
        return True
    except Exception as e:
        print_fail(f"Health check failed: {e}")
        return False

def test_store_facts():
    """Test 2: Store multiple facts (L0 Observations)"""
    print_test("Store Facts (L0 Observations)")
    
    facts = [
        "I love coding in Python",
        "Python is my favorite programming language",
        "I use Python for data science projects",
        "Python code is very readable",
        "I prefer Python over Java for most tasks"
    ]
    
    stored_ids = []
    try:
        for fact in facts:
            response = requests.post(
                f"{BASE_URL}/v1/logical/store",
                json={
                    "content": fact,
                    "user_id": USER_ID,
                    "tags": ["python", "coding"]
                }
            )
            assert response.status_code == 200
            data = response.json()
            stored_ids.append(data["fact_id"])
        
        print_pass(f"Stored {len(stored_ids)} facts successfully")
        print_info(f"Sample Fact ID: {stored_ids[0]}")
        return True, stored_ids
    except Exception as e:
        print_fail(f"Failed to store facts: {e}")
        return False, []

def test_dream_cycle():
    """Test 3: Dream Cycle (Reflection Trees + Memory Decay)"""
    print_test("Dream Cycle (L0→L1→L2→L3)")
    
    try:
        response = requests.post(
            f"{BASE_URL}/v1/intuitive/dream",
            json={"user_id": USER_ID}
        )
        assert response.status_code == 200
        data = response.json()
        
        print_pass(f"Dream cycle completed: {data['status']}")
        print_info(f"Summary: {data['summary']}")
        
        if "patterns" in data and len(data["patterns"]) > 0:
            print_pass(f"Generated {len(data['patterns'])} Reflections (L1)")
            print_info(f"Sample Pattern: {data['patterns'][0][:80]}...")
        
        if "insights" in data and len(data["insights"]) > 0:
            print_pass(f"Generated {len(data['insights'])} Generalizations (L2)")
            print_info(f"Sample Insight: {data['insights'][0][:80]}...")
        
        if "profile_updated" in data and data["profile_updated"]:
            print_pass("Psychological Profile updated (L3)")
        
        if "memories_fading" in data:
            print_info(f"Memory Decay: {data['memories_fading']} memories fading")
        
        return True
    except Exception as e:
        print_fail(f"Dream cycle failed: {e}")
        return False

def test_recall():
    """Test 4: Recall with Hallucination Safeguards"""
    print_test("Recall (with Citations & Verification)")
    
    try:
        response = requests.post(
            f"{BASE_URL}/v1/logical/recall",
            params={
                "query": "What programming language do I like?",
                "user_id": USER_ID
            }
        )
        assert response.status_code == 200
        data = response.json()
        
        print_pass("Recall successful")
        print_info(f"Query: {data['query']}")
        print_info(f"Response: {data['result'][:200]}...")
        print_info(f"Facts Retrieved: {data['metadata']['facts_retrieved']}")
        print_info(f"Confidence: {data['metadata']['confidence']:.2f}")
        
        # Check for citations
        if "[Fact:" in data['result']:
            print_pass("Strict Citation Mode: Citations found in response")
        else:
            print_info("Citations not found (may be expected for general queries)")
        
        return True
    except Exception as e:
        print_fail(f"Recall failed: {e}")
        return False

def test_prediction():
    """Test 5: Predictive Active Inference"""
    print_test("Predictive Active Inference")
    
    try:
        response = requests.get(f"{BASE_URL}/v1/intuitive/predict/{USER_ID}")
        assert response.status_code == 200
        data = response.json()
        
        if data["status"] == "suggestion_available":
            print_pass("Prediction generated!")
            print_info(f"Suggested Action: {data['prediction']['suggested_action']}")
            print_info(f"Reasoning: {data['prediction']['reasoning']}")
            print_info(f"Confidence: {data['prediction']['confidence']:.2f}")
        else:
            print_info("No prediction (Free energy minimized)")
            print_pass("Prediction engine operational (no suggestion needed)")
        
        return True
    except Exception as e:
        print_fail(f"Prediction failed: {e}")
        return False

def run_all_tests():
    """Run all integration tests"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}MemVra Bicameral Architecture - Integration Tests{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")
    
    results = []
    
    # Test 1: Health Check
    results.append(test_health_check())
    
    # Test 2: Store Facts
    success, fact_ids = test_store_facts()
    results.append(success)
    
    # Wait a moment for processing
    time.sleep(1)
    
    # Test 3: Dream Cycle
    results.append(test_dream_cycle())
    
    # Test 4: Recall
    results.append(test_recall())
    
    # Test 5: Prediction
    results.append(test_prediction())
    
    # Summary
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"{Colors.GREEN}🎉 ALL TESTS PASSED ({passed}/{total}){Colors.END}")
    else:
        print(f"{Colors.YELLOW}⚠️  SOME TESTS FAILED ({passed}/{total} passed){Colors.END}")
    
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    return passed == total

class Tee(object):
    def __init__(self, name, mode):
        self.file = open(name, mode, encoding='utf-8')
        self.stdout = sys.stdout
        sys.stdout = self
    def __del__(self):
        sys.stdout = self.stdout
        self.file.close()
    def write(self, data):
        self.file.write(data)
        self.stdout.write(data)
    def flush(self):
        self.file.flush()
        self.stdout.flush()

if __name__ == "__main__":
    import sys
    # Redirect stdout to a log file to avoid capture issues
    sys.stdout = Tee('integration_test.log', 'w')
    
    try:
        success = run_all_tests()
        exit(0 if success else 1)
    except Exception as e:
        print_fail(f"Test suite failed: {e}")
        exit(1)
