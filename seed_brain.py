"""
Simplified seed script for MemVra - Uses brain API directly
"""
import requests
import time

BRAIN_URL = "http://localhost:8000/v1"
USER_ID = "test@example.com"  # Use actual logged-in user

# Test facts representing realistic usage
TEST_FACTS = [
    "I prefer working in the morning, usually starting at 7 AM",
    "My favorite programming language is Python because of its readability",
    "I drink 3 cups of coffee every day - one in morning, one at lunch, one at 3pm",
    "Currently working on a machine learning project for image classification",
    "Team meeting scheduled every Monday at 10 AM to discuss sprint progress",
    "Completed the authentication module using JWT tokens last week",
    "Learning React and TypeScript to build modern web applications",
    "Read 'Clean Code' by Robert Martin - key takeaway: functions should do one thing well",
    "I go to the gym 4 times a week, focusing on strength training",
    "Love watching sci-fi movies, especially anything by Christopher Nolan",
    "Goal for this year: build a SaaS product from scratch and launch it",
    "Want to contribute more to open source projects, especially in AI/ML space",
    "I use VS Code as my primary IDE with Vim keybindings extension",
    "Prefer PostgreSQL over MySQL for relational databases - better JSON support",
    "Recently switched from REST to GraphQL for our API - much more flexible"
]

def seed_brain():
    """Store facts directly in brain"""
    print("🧠 Seeding brain with test memories...")
    print("=" * 60)
    
    stored = 0
    for i, content in enumerate(TEST_FACTS, 1):
        try:
            response = requests.post(
                f"{BRAIN_URL}/logical/store",
                params={"user_id": USER_ID},
                json={
                    "user_id": USER_ID,
                    "content": content,
                    "tags": []
                }
            )
            response.raise_for_status()
            print(f"✓ [{i:2d}/15] {content[:55]}...")
            stored += 1
            time.sleep(0.1)
        except Exception as e:
            print(f"✗ [{i:2d}/15] Failed: {str(e)[:60]}")
    
    print("=" * 60)
    print(f"✓ Successfully stored {stored}/15 memories in brain")
    return stored

def trigger_pattern_analysis():
    """Trigger dream cycle for pattern detection"""
    print("\n💭 Analyzing patterns (Dream Cycle)...")
    print("=" * 60)
    
    try:
        response = requests.post(
            f"{BRAIN_URL}/intuitive/dream",
            json={
                "user_id": USER_ID,
                "facts": TEST_FACTS
            }
        )
        response.raise_for_status()
        result = response.json()
        
        print("✓ Pattern analysis complete!")
        print(f"\n📊 Results:")
        print(f"  • Patterns discovered: {len(result.get('patterns', []))}")
        for i, pattern in enumerate(result.get('patterns', [])[:5], 1):
            print(f"    {i}. {pattern}")
        
        print(f"\n  • Sentiment: {result.get('sentiment', 'N/A')}")
        print(f"  • Consolidated memories: {result.get('consolidated_memories', 0)}")
        
        return result
    except Exception as e:
        print(f"✗ Pattern analysis failed: {e}")
        return None

def test_memory_recall():
    """Test brain's ability to recall information"""
    print("\n🔍 Testing Memory Recall...")
    print("=" * 60)
    
    queries = [
        "What are my hobbies and interests?",
        "Tell me about my work and projects",
        "What are my habits and routines?"
    ]
    
    for query in queries:
        try:
            response = requests.post(
                f"{BRAIN_URL}/logical/recall",
                params={"query": query, "user_id": USER_ID}
            )
            response.raise_for_status()
            result = response.json()
            
            print(f"\nQ: {query}")
            print(f"A: {result['result'][:120]}...")
            print(f"   (Retrieved {result['metadata']['facts_retrieved']} facts, confidence: {result['metadata']['confidence']:.2f})")
        except Exception as e:
            print(f"✗ Query failed: {e}")

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(" " * 15 + "MemVra Brain Seeder")
    print("=" * 60 + "\n")
    
    # Step 1: Store memories
    stored = seed_brain()
    
    if stored > 0:
        # Step 2: Analyze patterns
        patterns = trigger_pattern_analysis()
        
        # Step 3: Test recall
        test_memory_recall()
    
    print("\n" + "=" * 60)
    print("✓ Seeding Complete!")
    print("=" * 60)
    print("\n📌 Next Steps:")
    print("   1. Refresh dashboard to see brain stats")
    print("   2. Open chat widget and ask about your preferences")
    print("   3. Check /profile to see linguistic adaptation")
    print("   4. Note: Facts are in brain memory (not main DB)")
    print("\n" + "=" * 60 + "\n")
