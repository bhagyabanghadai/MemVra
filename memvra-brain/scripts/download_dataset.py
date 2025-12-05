# Dataset Integration Script
# Downloads and processes real user journal data for MemVra Brain

import pandas as pd
import json
import sys
from datetime import datetime, timedelta

print("MemVra Brain - Real Dataset Integration")
print("=" * 50)

# Instructions for manual download
print("""
DATASET: Journal Entries with Labelled Emotions
SOURCE: https://www.kaggle.com/datasets/madhavmalhotra/journal-entries-with-labelled-emotions

TO DOWNLOAD:
1. Visit the URL above
2. Click 'Download' (requires free Kaggle account)
3. Extract the CSV file to: memvra-brain/data/journal_emotions.csv

ALTERNATIVE - Install Kaggle API:
1. pip install kaggle
2. Get API key from https://www.kaggle.com/settings
3. Place kaggle.json in ~/.kaggle/ (or C:\\Users\\YourName\\.kaggle on Windows)
4. Run: kaggle datasets download -d madhavmalhotra/journal-entries-with-labelled-emotions
""")

# Check if data file exists
import os
data_path = "data/journal_emotions.csv"

if not os.path.exists("data"):
    os.makedirs("data")
    print("\nCreated data/ directory")

if os.path.exists(data_path):
    print(f"\n✅ Dataset found at {data_path}")
    print("\nProcessing data...")
    
    # Load the dataset
    df = pd.read_csv(data_path)
    
    print(f"\nDataset Statistics:")
    print(f"  Total entries: {len(df)}")
    print(f"  Columns: {', '.join(df.columns.tolist())}")
    
    # Preview first few entries
    print(f"\nSample entries:")
    print(df.head(3))
    
    # Convert to MemVra Brain format
    print("\nConverting to MemVra format...")
    
    memories = []
    base_date = datetime(2025, 1, 1)
    
    for idx, row in df.iterrows():
        # Assume the dataset has 'text' and emotion columns
        memory = {
            "fact_id": f"journal_{idx}",
            "content": str(row.get('text', row.get('entry', ''))),  # Try different column names
            "created_at": (base_date + timedelta(hours=idx)).isoformat(),
            "emotions": []  # Will be populated based on emotion columns
        }
        
        # Extract emotions (dataset has binary columns for each emotion)
        emotion_cols = ['happy', 'satisfied', 'calm', 'proud', 'excited', 
                       'frustrated', 'anxious', 'surprised', 'nostalgic', 'bored',
                       'sad', 'angry', 'confused', 'disgusted', 'afraid', 
                       'ashamed', 'awkward', 'jealous']
        
        for emotion in emotion_cols:
            if emotion in row and row[emotion] == 1:
                memory['emotions'].append(emotion)
        
        memories.append(memory)
    
    # Save processed data
    output_path = "data/processed_memories.json"
    with open(output_path, 'w') as f:
        json.dump(memories[:100], f, indent=2)  # Save first 100 for demo
    
    print(f"\n✅ Processed {len(memories)} memories")
    print(f"✅ Saved sample (100 entries) to {output_path}")
    
    # Create a test batch for the brain
    test_batch = {
        "facts": [
            {
                "fact_id": m['fact_id'],
                "content": m['content'],
                "created_at": m['created_at']
            }
            for m in memories[:10]  # First 10 entries
        ]
    }
    
    test_path = "data/test_batch.json"
    with open(test_path, 'w') as f:
        json.dump(test_batch, f, indent=2)
    
    print(f"✅ Created test batch (10 entries) at {test_path}")
    print("\nYou can now test this data with:")
    print("  $testData = Get-Content data/test_batch.json | ConvertFrom-Json | ConvertTo-Json -Depth 10")
    print("  Invoke-RestMethod -Uri 'http://localhost:8000/v1/intuitive/dream' -Method POST -Body $testData -ContentType 'application/json'")
    
else:
    print(f"\n⚠️  Dataset not found at {data_path}")
    print("\nPlease download the dataset first using the instructions above.")
    print("\nAfter downloading, rerun this script:")
    print("  python download_dataset.py")
