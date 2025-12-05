# MemVra Brain: Technical Architecture Documentation

## Overview
MemVra Brain is a groundbreaking AI memory system implementing a **Bicameral Predictive Architecture** that combines deep cognitive understanding with proactive intelligence. It surpasses existing solutions (Mem0, Claude) by integrating cutting-edge research in cognitive science, neuroscience, and machine learning.

## Core Philosophy
The system operates as a **dual-brain architecture**:
1. **Reflective Brain**: Deep understanding through hierarchical memory compression
2. **Predictive Brain**: Proactive assistance via Active Inference

---

## Architecture Layers

### Layer 0: Observations (Raw Facts)
**Purpose**: Store raw user interactions with full fidelity.

**Implementation**: [`bdh_graph.py`](file:///f:/Startup_Projects/MemVra/memvra-brain/core/bdh_graph.py)
- **Data Structure**: Graph nodes with semantic embeddings
- **Storage**: In-memory (can scale to graph DB like Neo4j)
- **Key Method**: `add_fact(fact_id, content, user_id, metadata)`

**Example**:
```python
{
  "fact_id": "fact_1234",
  "content": "I love coding in Python",
  "user_id": "user_abc",
  "created_at": "2024-12-04T10:30:00",
  "embedding": [0.234, -0.123, ...],  # 384-dim vector
  "metadata": {"version": "new", "stability": 0.5}
}
```

---

### Layer 1: Reflections (Patterns)
**Purpose**: Identify recurring patterns from observations.

**Research Basis**: Inspired by "Generative Agents" (Park et al., Stanford 2023)

**Implementation**: [`trm_compressor.py`](file:///f:/Startup_Projects/MemVra/memvra-brain/core/trm_compressor.py) → `generate_reflections()`

**Algorithm**:
1. Group facts by topic (keyword clustering)
2. For each topic with 3+ facts:
   - Extract pattern description
   - Calculate confidence score
3. Return patterns as Level 1 nodes

**Example Transformation**:
```
Input (L0):
  - "I love coding in Python"
  - "Python is my favorite language"
  - "I use Python for data science"

Output (L1):
  Pattern: "Coding_PREFERENCE → python, favorite, coding (from 3 facts)"
  Confidence: 0.6
```

---

### Layer 2: Generalizations (Insights)
**Purpose**: Synthesize high-level personality traits from patterns.

**Implementation**: `generate_generalizations()`

**Algorithm**:
1. Count topics across all patterns
2. Top 3 topics become generalizations
3. Calculate importance score

**Example**:
```
Input (L1): 10 patterns, 5 about "Coding", 3 about "UI", 2 about "Performance"

Output (L2):
  - "User shows strong coding focus (50% of patterns)"
  - "User has UI design interest (30% of patterns)"
```

---

### Layer 3: Psychological Profile (Theory of Mind)
**Purpose**: Model user's beliefs, intents, and emotional states.

**Research Basis**: "Theory of Mind in Large Language Models" (Kosinski, 2023)

**Implementation**: `synthesize_psychological_profile()`

**Schema**:
```python
{
  "user_id": "user_abc",
  "traits": ["Productivity", "Coding", "Efficiency"],
  "beliefs": ["Believes Coding is important", "Believes Productivity is important"],
  "intents": ["Improve productivity", "Learn new things"],
  "emotions": ["Curious", "Determined"]
}
```

**Storage**: Graph node linked to Level 2 generalizations

---

## Memory Lifecycle System

### SM-2 Algorithm (Spaced Repetition)
**Purpose**: Score memory importance based on recall quality.

**Research**: Wozniak, 1990 (SuperMemo)

**Implementation**: `calculate_memory_score(quality, previous_ease, previous_interval)`

**Formula**:
```
EF' = EF + (0.1 - (5 - q) × (0.08 + (5 - q) × 0.02))
EF' = max(1.3, EF')

Interval:
  - If previous_interval = 0: new_interval = 1
  - If previous_interval = 1: new_interval = 6
  - Else: new_interval = previous_interval × EF'

Stability = min(1.0, interval / 30)
```

**Parameters**:
- `quality`: 0-5 (5 = perfect recall, 0 = forgot)
- `previous_ease`: Ease Factor (default 2.5)
- `previous_interval`: Days since last recall

**Output**:
```python
{
  "ease_factor": 2.6,
  "interval": 15,  # days
  "stability": 0.5  # 0.0-1.0
}
```

---

### Ebbinghaus Forgetting Curve
**Purpose**: Simulate natural memory decay over time.

**Research**: Hermann Ebbinghaus, 1885

**Implementation**: `apply_ebbinghaus_decay(memory_nodes, days_elapsed)`

**Formula**:
```
R = e^(-t/S)

Where:
  R = Retention (0.0-1.0)
  t = Time elapsed (days)
  S = Stability score × 10 (scaled to days)
```

**Example**:
```python
# Memory with stability 0.5, after 30 days
strength = 0.5 × 10 = 5
retention = e^(-30/5) = e^(-6) = 0.0025

# Status: "fading" (retention < 0.3)
```

**Integration**: Runs during `/v1/intuitive/dream` endpoint

---

## Predictive Active Inference

### Free Energy Principle
**Purpose**: Minimize "surprise" by predicting user needs.

**Research**: Karl Friston, 2010

**Implementation**: [`predictive_engine.py`](file:///f:/Startup_Projects/MemVra/memvra-brain/core/predictive_engine.py)

**Core Concept**:
The brain constantly predicts sensory input. When predictions fail, "surprise" (free energy) increases. The system learns to minimize this by updating its internal model.

**Algorithm**:
1. **Observe**: Record query patterns (time, context)
2. **Predict**: Generate expected user need based on:
   - Psychological Profile (traits, intents)
   - Temporal context (time of day, day of week)
3. **Suggest**: If confidence > threshold (0.3), return suggestion
4. **Learn**: Update model based on user feedback

**Example Logic**:
```python
if "Productivity" in traits and 8 <= current_hour <= 10:
    return {
        "suggested_action": "Enable Focus Mode",
        "confidence": 0.85,
        "reasoning": "User values productivity and it is morning work hours"
    }
```

**Safety**: Human-in-the-Loop
- System only **suggests** actions
- Never **executes** external actions (booking, buying, etc.)
- Requires explicit user confirmation

---

## Hallucination Prevention

### 1. Strict Citation Mode
**Purpose**: Force LLM to cite sources for every claim.

**Implementation**: Modified prompt in `llama_service.py` → `stream_response()`

**Prompt Addition**:
```
STRICT CITATION: You MUST cite the source fact ID for every claim using [Fact: <id>].
```

**Facts Format**:
```
[Fact: fact_1234] I love coding in Python
[Fact: fact_5678] Python is my favorite language
```

**Expected Output**:
```
Based on your memories [Fact: fact_1234], you love coding in Python, 
and [Fact: fact_5678] it's your favorite language.
```

---

### 2. Self-Verification Loop
**Purpose**: Verify LLM output matches retrieved facts.

**Implementation**: `verify_response(response, facts)`

**Algorithm**:
1. Extract all facts into context
2. Send to verification LLM with prompt:
   ```
   Check: Does Response contain claims not in Context?
   Return: {supported: true/false, reason: "..."}
   ```
3. If `supported == false`, append warning to user

**Example**:
```python
verification = llama_service.verify_response(
    "You love Python and Java",
    [{"content": "I love Python"}]
)
# Returns: {supported: false, reason: "Java not mentioned in facts"}
```

---

## API Endpoints

### 1. Store Facts
**Endpoint**: `POST /v1/logical/store`

**Purpose**: Add new observations (L0)

**Request**:
```json
{
  "content": "I love coding in Python",
  "user_id": "user_123",
  "tags": ["coding", "python"]
}
```

**Response**:
```json
{
  "status": "success",
  "fact_id": "fact_1234"
}
```

---

### 2. Recall
**Endpoint**: `POST /v1/logical/recall?query=...&user_id=...`

**Purpose**: Retrieve and format memories

**Features**:
- Tiered retrieval (L2 → L1 → L0 fallback)
- Memory score reinforcement (SM-2 update on recall)
- Self-verification loop
- Strict citation mode

**Response**:
```json
{
  "query": "What do I like?",
  "result": "Based on [Fact: fact_1234], you love Python...",
  "metadata": {
    "facts_retrieved": 3,
    "confidence": 0.92
  }
}
```

---

### 3. Dream Cycle
**Endpoint**: `POST /v1/intuitive/dream`

**Purpose**: Background cognitive processing

**Operations**:
1. Generate Reflections (L0 → L1)
2. Generate Generalizations (L1 → L2)
3. Update Psychological Profile (L2 → L3)
4. Apply Memory Decay (Ebbinghaus)

**Response**:
```json
{
  "status": "success",
  "summary": "Processed 15 facts",
  "patterns": ["Coding_PREFERENCE → python..."],
  "insights": ["User shows strong coding focus..."],
  "profile_updated": true,
  "memories_fading": 2,
  "graph_stats": {...}
}
```

---

### 4. Predict
**Endpoint**: `GET /v1/intuitive/predict/{user_id}`

**Purpose**: Get proactive suggestions

**Response (Suggestion Available)**:
```json
{
  "status": "suggestion_available",
  "prediction": {
    "suggested_action": "Enable Focus Mode",
    "confidence": 0.85,
    "reasoning": "User values productivity and it is morning work hours"
  }
}
```

**Response (No Suggestion)**:
```json
{
  "status": "no_suggestion",
  "message": "Free energy is minimized (no surprise anticipated)"
}
```

---

## Key Components

### BDHGraph (Scale-Free Network)
**File**: [`bdh_graph.py`](file:///f:/Startup_Projects/MemVra/memvra-brain/core/bdh_graph.py)

**Features**:
- Semantic embeddings (SentenceTransformer)
- Hierarchical levels (0-3)
- Hub node detection (O(log n) retrieval)
- Similarity-based edge creation

**Methods**:
- `add_fact()`: Add L0 node
- `add_pattern()`: Add L1 node
- `add_insight()`: Add L2 node
- `add_psychological_profile()`: Add L3 node
- `retrieve()`: Multi-level retrieval with fallback
- `update_fact_stats()`: Update SM-2 scores

---

### TRMCompressor (Hierarchical Compression)
**File**: [`trm_compressor.py`](file:///f:/Startup_Projects/MemVra/memvra-brain/core/trm_compressor.py)

**Methods**:
- `generate_reflections()`: L0 → L1
- `generate_generalizations()`: L1 → L2
- `synthesize_psychological_profile()`: L2 → L3
- `calculate_memory_score()`: SM-2 algorithm
- `apply_ebbinghaus_decay()`: Memory decay

---

### LlamaService (LLM Integration)
**File**: [`llama_service.py`](file:///f:/Startup_Projects/MemVra/memvra-brain/core/llama_service.py)

**Model**: Llama 3.1 8B (via Ollama)

**Methods**:
- `enhance_query()`: Extract intent/keywords
- `stream_response()`: Generate response with citations
- `verify_response()`: Self-verification loop
- `format_response()`: Legacy non-streaming wrapper

---

## Performance Characteristics

### Retrieval Latency (Target)
- **Fast Path** (<50ms): Cache (not yet implemented)
- **Medium Path** (<200ms): Vector search on L1/L2
- **Slow Path** (>500ms): Full graph traversal

### Compression Ratios
- **L0 → L1**: ~5:1 (5 facts → 1 pattern)
- **L1 → L2**: ~3:1 (3 patterns → 1 generalization)
- **Overall**: ~15:1 compression

---

## Research Citations

1. **Reflection Trees**: Park et al., "Generative Agents: Interactive Simulacra of Human Behavior", Stanford, 2023
2. **SM-2 Algorithm**: Wozniak, "SuperMemo Algorithm SM-2", 1990
3. **Ebbinghaus Curve**: Ebbinghaus, "Memory: A Contribution to Experimental Psychology", 1885
4. **Theory of Mind**: Kosinski, "Theory of Mind May Have Spontaneously Emerged in Large Language Models", 2023
5. **Active Inference**: Friston, "The Free-Energy Principle: A Unified Brain Theory?", 2010

---

## Future Enhancements

1. **Database Integration**
   - PostgreSQL for fact storage
   - Neo4j for graph relationships
   - Redis for caching

2. **Advanced Reflection**
   - Replace keyword clustering with LLM-based semantic reflection
   - Multi-hop reasoning across graph

3. **Asynchronous Processing**
   - Background dream cycle worker
   - Real-time decay updates

4. **Enhanced Prediction**
   - Bayesian belief networks
   - Temporal pattern recognition (daily/weekly cycles)
