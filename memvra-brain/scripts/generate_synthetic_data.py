# Generate Realistic Synthetic Memory Dataset
# Based on patterns from real journal entry data

import json
from datetime import datetime, timedelta
import random

print("Generating realistic memory dataset...")

# Realistic memory templates based on actual journal entries
memory_templates = [
    # Productive/Happy memories
    {
        "content": "Had a great day at work today. Successfully completed the authentication feature I've been working on. Team appreciated my contributions during the code review.",
        "emotions": ["happy", "satisfied", "proud"]
    },
    {
        "content": "Woke up early and went for a run. Felt energized throughout the day. Managed to finish all my tasks ahead of schedule.",
        "emotions": ["happy", "excited", "satisfied"]
    },
    {
        "content": "Spent quality time with family this evening. We had dinner together and shared stories from our week. These moments remind me what's truly important.",
        "emotions": ["happy", "calm", "nostalgic"]
    },
    
    # Stressed/Frustrated memories
    {
        "content": "Dealing with a critical bug in production. Users are reporting login failures. Spent hours debugging but haven't found the root cause yet. Feeling stressed.",
        "emotions": ["frustrated", "anxious", "confused"]
    },
    {
        "content": "Had a disagreement with a colleague about the project direction. The meeting didn't go well. I feel like my suggestions aren't being heard.",
        "emotions": ["frustrated", "angry", "disappointed"]
    },
    {
        "content": "Database performance issues are getting worse. Every query is slow. Management is pushing for faster delivery but the infrastructure isn't ready.",
        "emotions": ["frustrated", "anxious", "overwhelmed"]
    },
    
    # Mixed/Reflective memories
    {
        "content": "This week has been challenging but I learned a lot. The optimization work was harder than expected, but seeing the performance improvements makes it worthwhile.",
        "emotions": ["satisfied", "tired", "proud"]
    },
    {
        "content": "Mentor session went well. Helping junior developers reminds me how far I've come. Sometimes you need to look back to appreciate progress.",
        "emotions": ["proud", "nostalgic", "satisfied"]
    },
    {
        "content": "Finished reading a technical book on system design. Some concepts are still unclear, but I'm starting to see patterns in how large systems are built.",
        "emotions": ["curious", "confused", "excited"]
    },
    
    # Neutral/Daily life
    {
        "content": "Routine day at the office. Attended meetings, reviewed some code, replied to emails. Nothing particularly exciting or frustrating.",
        "emotions": ["calm", "neutral"]
    },
    {
        "content": "Working on documentation today. Not the most exciting task, but it needs to be done. At least I can listen to music while writing.",
        "emotions": ["bored", "calm"]
    },
]

# Generate 100,000 realistic memories (Lifetime Scale)
memories = []
base_date = datetime(2020, 1, 1) # Start further back

print("Generating 100,000 memories (this may take a moment)...")
for i in range(100000):
    template = random.choice(memory_templates)
    
    # Add some variation to the content
    content = template["content"]
    
    memory = {
        "fact_id": f"synthetic_{i:06d}",
        "content": content,
        "created_at": (base_date + timedelta(hours=i*0.5)).isoformat(),
        "emotions": template["emotions"]
    }
    
    memories.append(memory)

# Save full dataset
output_path = "data/synthetic_memories_100k.json"
with open(output_path, 'w') as f:
    json.dump(memories, f, indent=2)

print(f"✅ Generated {len(memories)} realistic memories")
print(f"✅ Saved to {output_path}")

# Create test batches of different sizes
test_batches = {
    "small": memories[:5],
    "medium": memories[:20],
    "large": memories[:50],
    "extra_large": memories[:100],
    "full": memories[:200],
    "massive": memories[:2000],
    "mega": memories[:10000],
    "ultra": memories[:50000],
    "lifetime": memories # 100,000
}

for size, batch in test_batches.items():
    test_data = {
        "facts": [
            {
                "fact_id": m["fact_id"],
                "content": m["content"],
                "created_at": m["created_at"]
            }
            for m in batch
        ]
    }
    
    batch_path = f"data/test_batch_{size}.json"
    with open(batch_path, 'w') as f:
        json.dump(test_data, f, indent=2)
    
    print(f"✅ Created {size} test batch ({len(batch)} entries) at {batch_path}")

print("\n" + "="*50)
print("READY TO TEST!")
print("="*50)
print("\nRun this command to test with 20 realistic memories:")
print("  cd memvra-brain")
print("  $data = Get-Content data/test_batch_medium.json | ConvertFrom-Json | ConvertTo-Json -Depth 10")
print("  Invoke-RestMethod -Uri 'http://localhost:8000/v1/intuitive/dream' -Method POST -Body $data -ContentType 'application/json'")
