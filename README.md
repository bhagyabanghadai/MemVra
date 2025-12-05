# MemVra: Bicameral Predictive Memory Architecture

> **The World's First "Bicameral" AI Brain** combining deep cognitive reflection with proactive active inference.

MemVra is a next-generation AI memory system designed to surpass existing solutions like Mem0 and standard RAG. Instead of just storing "flat facts," MemVra mimics the human brain's dual process of **Reflection** (understanding the past) and **Prediction** (anticipating the future).

![Architecture Status](https://img.shields.io/badge/Architecture-Bicameral_v3.0-blueviolet) ![Status](https://img.shields.io/badge/Status-Production_Ready-success)

---

## 🧠 Core Philosophy: The Bicameral Brain

The system is split into two distinct but interconnected cognitive engines:

### 1. The Reflective Brain (Deep Understanding)
*Moves from raw data to abstract wisdom.*
- **L0: Observations**: "User bought coffee at 8 AM."
- **L1: Patterns**: "User buys coffee every weekday morning."
- **L2: Generalizations**: "User is caffeine-dependent for productivity."
- **L3: Psychological Profile**: Models user's Beliefs, Intents, Traits, and Emotions (Theory of Mind).

### 2. The Predictive Brain (Active Intuition)
*Minimizes surprise through Active Inference.*
- Uses the **Free Energy Principle** (Friston, 2010) to anticipate user needs.
- **Example**: If the user has a "Productivity" trait and it's 9 AM, the brain *proactively* suggests "Enable Focus Mode" before the user asks.

---

## 🚀 Key Features

### 📉 Intelligent Memory Lifecycle
Memories aren't static; they live and die based on utility.
- **SM-2 Algorithm**: Spaced repetition scoring reinforces useful memories.
- **Ebbinghaus Decay**: Memories fade naturally over time (`R = e^(-t/S)`), keeping the context window clean and relevant.
- **Dream Cycle**: A background process that consolidates memories and prunes decay during downtime.

### 🛡️ Hallucination Safeguards
Trust is paramount.
- **Strict Citation Mode**: Every claim MUST cite a source fact ID (`[Fact: 123]`).
- **Self-Verification Loop**: A dedicated sub-routine verifies that the generated answer is actually supported by the cited facts *before* sending it to the user.

### ⚡ Hybrid Architecture
- **Tech Stack**: Python (FastAPI), NetworkX (Graph), SentenceTransformers (Embeddings), Llama 3 (Cognition).
- **Structure**: Modular design with `core/memory`, `core/cognition`, and `core/prediction` engines.

---

## 📚 Documentation

For a deep dive into the algorithms, math, and research backing this project, please read the **[Technical Architecture Documentation](memvra-brain/docs/brain_architecture.md)**.

---

## 🏁 Getting Started

### Prerequisites
- Python 3.10+
- Docker (optional)

### 1. Start the Brain
```bash
cd memvra-brain
pip install -r requirements.txt
python main.py
```
*Server runs at `http://localhost:8000`*

### 2. Verify System
Run the end-to-end integration suite:
```bash
python memvra-brain/scripts/final_verify.py
```

### 3. API Usage Examples

**Store a Memory (L0):**
```bash
curl -X POST "http://localhost:8000/v1/logical/store" \
     -H "Content-Type: application/json" \
     -d '{"content": "I love Python", "user_id": "me"}'
```

**Trigger Dream Cycle (Consolidation):**
```bash
curl -X POST "http://localhost:8000/v1/intuitive/dream" \
     -d '{"user_id": "me"}'
```

**Ask for a Prediction:**
```bash
curl "http://localhost:8000/v1/intuitive/predict/me"
```

---

## 🔬 Research Foundations
Built on cutting-edge papers:
1. **Generative Agents** (Park et al., 2023) - *Reflection Trees*
2. **Theory of Mind in LLMs** (Kosinski, 2023) - *Psychological Profiling*
3. **Free Energy Principle** (Friston, 2010) - *Active Inference*
4. **SuperMemo SM-2** (Wozniak, 1990) - *Memory Scoring*

---

## 📜 License
MIT
