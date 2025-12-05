"""
Seed realistic test data for MemVra demonstration
"""
import requests
import time

BASE_URL = "http://localhost:8080/v1"
BRAIN_URL = "http://localhost:8000/v1"

# Test facts representing a realistic user scenario
TEST_FACTS = [
    # Personal preferences
    {
        "content": "I prefer working in the morning, usually starting at 7 AM",
        "source_type": "user_input",
        "source_id": "preference-001",
        "recorded_by": "user-self"
    },
    {
        "content": "My favorite programming language is Python because of its readability",
        "source_type": "user_input",
        "source_id": "preference-002",
        "recorded_by": "user-self"
    },
    {
        "content": "I drink 3 cups of coffee every day - one in morning, one at lunch, one at 3pm",
        "source_type": "user_input",
        "source_id": "habit-001",
        "recorded_by": "user-self"
    },
    # Work activities
    {
        "content": "Currently working on a machine learning project for image classification",
        "source_type": "user_input",
        "source_id": "work-001",
        "recorded_by": "user-self"
    },
    {
        "content": "Team meeting scheduled every Monday at 10 AM to discuss sprint progress",
        "source_type": "user_input",
        "source_id": "schedule-001",
        "recorded_by": "user-self"
    },
    {
        "content": "Completed the authentication module using JWT tokens last week",
        "source_type": "user_input",
        "source_id": "achievement-001",
        "recorded_by": "user-self"
    },
    # Learning and growth
    {
        "content": "Learning React and TypeScript to build modern web applications",
        "source_type": "user_input",
        "source_id": "learning-001",
        "recorded_by": "user-self"
    },
    {
        "content": "Read 'Clean Code' by Robert Martin - key takeaway: functions should do one thing well",
        "source_type": "user_input",
        "source_id": "learning-002",
        "recorded_by": "user-self"
    },
    # Personal life
    {
        "content": "I go to the gym 4 times a week, focusing on strength training",
        "source_type": "user_input",
        "source_id": "health-001",
        "recorded_by": "user-self"
    },
    {
        "content": "Love watching sci-fi movies, especially anything by Christopher Nolan",
        "source_type": "user_input",
        "source_id": "entertainment-001",
        "recorded_by": "user-self"
    },
    # Goals and aspirations
    {
        "content": "Goal for this year: build a SaaS product from scratch and launch it",
        "source_type": "user_input",
        "source_id": "goal-001",
        "recorded_by": "user-self"
    },
    {
        "content": "Want to contribute more to open source projects, especially in AI/ML space",
        "source_type": "user_input",
        "source_id": "goal-002",
        "recorded_by": "user-self"
    },
    # Technical preferences
    {
        "content": "I use VS Code as my primary IDE with Vim keybindings extension",
        "source_type": "user_input",
        "source_id": "tools-001",
        "recorded_by": "user-self"
    },
    {
        "content": "Prefer PostgreSQL over MySQL for relational databases - better JSON support",
        "source_type": "user_input",
        "source_id": "tools-002",
        "recorded_by": "user-self"
    },
    {
        "content": "Recently switched from REST to GraphQL for our API - much more flexible",
        "source_type": "user_input",
        "source_id": "tech-decision-001",
        "recorded_by": "user-self"
    }
]

def seed_facts():
    """Insert test facts into the system"""
    print("🌱 Seeding test data...")
    print("-" * 50)
    
    fact_ids = []
    for i, fact in enumerate(TEST_FACTS, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/facts",
                json=fact,
                headers={
                    'X-API-Key': 'local-dev-api-key',
                    'Content-Type': 'application/json'
                }
            )
            response.raise_for_status()
            result = response.json()
            fact_ids.append(result['fact_id'])
            print(f"✓ [{i:2d}/15] {fact['content'][:60]}...")
            time.sleep(0.2)  # Small delay to avoid overwhelming the server
        except Exception as e:
            print(f"✗ [{i:2d}/15] Failed: {e}")
    
    print("-" * 50)
    print(f"✓ Successfully seeded {len(fact_ids)} facts")
    return fact_ids

def store_in_brain():
    """Store facts in brain for memory compression"""
    print("\n🧠 Storing facts in brain...")
    print("-" * 50)
    
    try:
        for fact in TEST_FACTS:
            response = requests.post(
                f"{BRAIN_URL}/logical/store",
                params={
                    "user_id": "default"
                },
                json={
                    "user_id": "default",
                    "content": fact['content'],
                    "tags": []
                }
            )
            response.raise_for_status()
            result = response.json()
            print(f"✓ Stored: {fact['content'][:60]}...")
            time.sleep(0.1)
        
        print("-" * 50)
        print("✓ All facts stored in brain")
        return True
    except Exception as e:
        print(f"✗ Brain storage failed: {e}")
        return False

def trigger_dream_cycle():
    """Trigger brain's dream cycle for pattern detection"""
    print("\n💭 Triggering dream cycle...")
    print("-" * 50)
    
    try:
        response = requests.post(
            f"{BRAIN_URL}/intuitive/dream",
            json={
                "user_id": "default",
                "facts": [f['content'] for f in TEST_FACTS]
            }
        )
        response.raise_for_status()
        result = response.json()
        
        print("✓ Dream cycle complete!")
        print(f"\nPatterns discovered: {len(result.get('patterns', []))}")
        for i, pattern in enumerate(result.get('patterns', []), 1):
            print(f"  {i}. {pattern}")
        
        print(f"\nSentiment: {result.get('sentiment', 'N/A')}")
        print(f"Consolidated memories: {result.get('consolidated_memories', 0)}")
        
        return result
    except Exception as e:
        print(f"✗ Dream cycle failed: {e}")
        return None

def test_recall():
    """Test brain recall with seeded data"""
    print("\n🔍 Testing brain recall...")
    print("-" * 50)
    
    test_queries = [
        "What are my hobbies?",
        "What do I do for work?",
        "What are my goals?"
    ]
    
    for query in test_queries:
        try:
            response = requests.post(
                f"{BRAIN_URL}/logical/recall",
                params={"query": query, "user_id": "default"}
            )
            response.raise_for_status()
            result = response.json()
            
            print(f"\nQuery: {query}")
            print(f"Response: {result['result'][:150]}...")
            print(f"Facts retrieved: {result['metadata']['facts_retrieved']}")
            print(f"Confidence: {result['metadata']['confidence']:.2f}")
        except Exception as e:
            print(f"✗ Recall failed: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("MemVra Test Data Seeder")
    print("=" * 50)
    
    # Step 1: Seed facts into main database
    fact_ids = seed_facts()
    
    # Step 2: Store in brain for compression
    brain_stored = store_in_brain()
    
    # Step 3: Trigger pattern analysis
    if brain_stored:
        dream_result = trigger_dream_cycle()
    
    # Step 4: Test recall
    test_recall()
    
    print("\n" + "=" * 50)
    print("✓ Seeding complete!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Open dashboard to see brain statistics")
    print("2. Navigate to /explore to browse facts")
    print("3. Try the chat widget to query your memories")
    print("4. Check /profile to see linguistic adaptation")
