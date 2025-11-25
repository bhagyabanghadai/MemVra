from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import sys
import os
from datetime import datetime
from collections import Counter
import re

# Add models to path
sys.path.append(os.path.join(os.path.dirname(__file__), "models"))

app = FastAPI(title="MemVra Brain", version="0.1.0")

# In-memory storage for demonstration
memory_store = {}

class FactInput(BaseModel):
    content: str
    fact_id: str
    created_at: str

class DreamInput(BaseModel):
    facts: List[FactInput]

class InsightOutput(BaseModel):
    summary: str
    patterns: List[str]
    sentiment: str
    consolidated_memories: Optional[int] = None
    key_insights: Optional[List[str]] = None

@app.get("/")
async def root():
    return {"status": "online", "brain": "bicameral", "memories_stored": len(memory_store)}

@app.post("/v1/logical/recall")
async def recall(query: str):
    """
    Logical Brain (BabyDragon): Precise fact retrieval
    Searches memory store for exact or fuzzy matches
    """
    query_lower = query.lower()
    
    # Search stored memories
    matches = []
    for fact_id, fact in memory_store.items():
        if query_lower in fact['content'].lower():
            matches.append({
                "fact_id": fact_id,
                "content": fact['content'],
                "created_at": fact['created_at'],
                "relevance": "exact" if query_lower == fact['content'].lower() else "partial"
            })
    
    if matches:
        return {
            "query": query,
            "result": f"Found {len(matches)} memory(ies)",
            "matches": matches[:5]  # Return top 5
        }
    else:
        return {
            "query": query,
            "result": "No exact memories found. Logical brain ready for new facts.",
            "suggestion": "Store facts first to enable recall"
        }

@app.post("/v1/intuitive/dream", response_model=InsightOutput)
async def dream(input_data: DreamInput):
    """
    Intuitive Brain (TinyRecursive): Pattern detection and consolidation
    Analyzes memories for themes, sentiment, and creates summaries
    """
    
    # Store facts in memory
    for fact in input_data.facts:
        memory_store[fact.fact_id] = {
            "content": fact.content,
            "created_at": fact.created_at
        }
    
    # Analyze patterns
    all_text = " ".join([f.content.lower() for f in input_data.facts])
    
    # Detect keywords and themes
    words = re.findall(r'\b\w+\b', all_text)
    word_freq = Counter(words)
    
    # Remove common words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'is', 'was', 'are', 'been', 'be', 'have', 'has', 'had'}
    significant_words = {word: count for word, count in word_freq.items() if word not in stop_words and len(word) > 3}
    top_themes = sorted(significant_words.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Detect sentiment
    positive_words = ['fixed', 'completed', 'optimized', 'success', 'working', 'improved', 'fast', 'good']
    negative_words = ['bug', 'error', 'slow', 'failed', 'issue', 'problem', 'crash']
    
    positive_count = sum(1 for word in positive_words if word in all_text)
    negative_count = sum(1 for word in negative_words if word in all_text)
    
    if positive_count > negative_count * 1.5:
        sentiment = "positive-productive"
    elif negative_count > positive_count * 1.5:
        sentiment = "negative-debugging"
    else:
        sentiment = "neutral-focused"
    
    # Generate patterns
    patterns = []
    
    # Detect coding activity
    if any(word in all_text for word in ['code', 'coding', 'develop', 'implement', 'feature']):
        patterns.append("Active development session detected")
    
    # Detect debugging
    if any(word in all_text for word in ['bug', 'fix', 'debug', 'error']):
        patterns.append("Problem-solving and debugging activity")
    
    # Detect performance work
    if any(word in all_text for word in ['optim', 'performance', 'speed', 'fast', 'slow']):
        patterns.append("Performance optimization focus")
    
    # Detect completion
    if any(word in all_text for word in ['completed', 'finished', 'done', 'working']):
        patterns.append("Task completion indicators present")
    
    # Generate key insights
    key_insights = []
    if top_themes:
        key_insights.append(f"Primary focus: {top_themes[0][0]}")
    if len(input_data.facts) > 3:
        key_insights.append(f"High activity period: {len(input_data.facts)} memories consolidated")
    
    # Create summary
    fact_count = len(input_data.facts)
    themes_str = ", ".join([theme[0] for theme in top_themes[:3]])
    summary = f"Consolidated {fact_count} memories. Detected themes: {themes_str}. Session appears {sentiment.replace('-', ' and ')}."
    
    return {
        "summary": summary,
        "patterns": patterns if patterns else ["General activity detected"],
        "sentiment": sentiment,
        "consolidated_memories": fact_count,
        "key_insights": key_insights
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
