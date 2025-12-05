from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from datetime import datetime
import json
from typing import List, Dict

from api.schemas import FactInput, DreamInput
# Import core modules - assuming they are still in the root core/ for now
from core.user_profile import UserProfile
from core.bdh_graph import BDHGraph
from core.trm_compressor import TRMCompressor
from core.llama_service import LlamaService
from core.confidence_manager import ConfidenceManager
from core.linguistic_profiler import LinguisticProfiler
from core.predictive_engine import PredictiveEngine
from core.bidirectional_learner import BidirectionalLearner
from core.temporal_tracker import TemporalTracker

router = APIRouter()

# Initialize Brain Components (Singletons)
# In a real app, these might be dependencies
bdh_graph = BDHGraph()
trm_compressor = TRMCompressor()
llama_service = LlamaService()
confidence_manager = ConfidenceManager()
linguistic_profiler = LinguisticProfiler()
predictive_engine = PredictiveEngine()
bidirectional_learner = BidirectionalLearner()
temporal_tracker = TemporalTracker()

# In-memory storage (Legacy support during migration)
user_profiles: Dict[str, UserProfile] = {}
memory_store = []

# Helper Functions
def get_user_profile(user_id: str) -> UserProfile:
    """Get or create user profile"""
    if user_id not in user_profiles:
        user_profiles[user_id] = UserProfile(user_id=user_id)
    return user_profiles[user_id]

def get_user_facts(user_id: str) -> List[Dict]:
    """Get all facts for a user"""
    return [fact for fact in memory_store if fact.get("user_id") == user_id]

@router.get("/")
async def root():
    return {
        "service": "MemVra Brain",
        "version": "3.0 (Bicameral Architecture)",
        "status": "operational"
    }

@router.post("/v1/logical/recall")
async def recall_optimized(query: str, user_id: str = "default"):
    try:
        user_profile = get_user_profile(user_id)
        user_profile.increment_query_count()
        
        # Predictive Engine Hook (Phase 3)
        predictive_engine.record_query_pattern(
            user_id, query, datetime.now(), user_profile
        )
        
        standardized_query = linguistic_profiler.understand_query(query, user_profile)
        enhanced = llama_service.enhance_query(standardized_query, user_profile.to_dict())
        
        results = bdh_graph.retrieve(
            query=enhanced["enhanced_query"],
            user_id=user_id,
            level=2
        )
        
        if results["facts"]:
            response_text = llama_service.format_response(
                facts=results["facts"],
                query=query,
                level_used=results["level"],
                confidence=results["confidence"],
                user_profile=user_profile.to_dict()
            )
            
            # Feature: Self-Verification Loop (Hallucination Safeguard)
            verification = llama_service.verify_response(response_text, results["facts"])
            if not verification.get("supported", True):
                response_text += f"\n\n[System Note: Verification Warning - {verification.get('reason', 'Potential inaccuracy detected')}]"
            
            # Feature: Update Memory Scores (Reinforcement)
            # When a fact is recalled, it's "Active Recall", so we boost its score
            for fact in results["facts"]:
                # Get current stats (mocked for now, would come from DB)
                current_ease = fact.get("ease_factor", 2.5)
                current_interval = fact.get("interval", 0)
                
                # Calculate new score (Quality=5 because it was successfully recalled)
                new_stats = trm_compressor.calculate_memory_score(5, current_ease, current_interval)
                
                # Update fact in graph (Conceptual)
                bdh_graph.update_fact_stats(fact["fact_id"], new_stats)
            
            response_text = linguistic_profiler.adapt_response(response_text, user_profile)
        else:
            response_text = f"I don't have any memories about '{query}' yet."
        
        return {
            "query": query,
            "result": response_text,
            "metadata": {
                "facts_retrieved": len(results["facts"]),
                "confidence": results["confidence"]
            }
        }
    except Exception as e:
        print(f"Error in recall: {e}")
        return {"result": f"Error: {str(e)}"}

@router.post("/v1/logical/store")
async def store_fact(fact_input: FactInput):
    try:
        user_profile = get_user_profile(fact_input.user_id)
        user_profile.increment_fact_count()
        
        fact_id = f"fact_{datetime.now().timestamp()}_{user_profile.total_facts}"
        
        # Temporal Versioning
        version_info = temporal_tracker.record_fact_version(
            fact_input.content, fact_input.user_id, fact_id
        )
        
        fact_data = {
            "fact_id": fact_id,
            "user_id": fact_input.user_id,
            "content": fact_input.content,
            "tags": fact_input.tags,
            "created_at": datetime.now().isoformat(),
            "metadata": {"version": version_info.get("type")}
        }
        memory_store.append(fact_data)
        
        bdh_graph.add_fact(
            fact_id=fact_id,
            content=fact_input.content,
            user_id=fact_input.user_id,
            metadata=fact_data["metadata"]
        )
        
        return {"status": "success", "fact_id": fact_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/v1/intuitive/dream")
async def dream_cycle(dream_input: DreamInput):
    """
    Background compression cycle (TRM)
    - Level 0 → L1 (Reflections)
    - Level 1 → L2 (Generalizations)
    - Level 2 → L3 (Psychological Profile)
    """
    try:
        user_profile = get_user_profile(dream_input.user_id)
        user_facts = get_user_facts(dream_input.user_id)
        
        if len(user_facts) < 5:
            return {
                "status": "skipped",
                "message": "Need more facts for pattern detection (minimum: 5)"
            }
        
        # Step 1: Compress Level 0 → Level 1 (Reflections)
        patterns = trm_compressor.generate_reflections(user_facts, dream_input.user_id)
        
        for i, pattern in enumerate(patterns):
            pattern_id = f"pattern_{dream_input.user_id}_{i}"
            bdh_graph.add_pattern(
                pattern_id=pattern_id,
                pattern=pattern["pattern"],
                facts_compressed=pattern["facts_compressed"],
                confidence=pattern["confidence"],
                user_id=dream_input.user_id
            )
        
        user_profile.total_patterns = len(patterns)
        
        # Step 2: Compress Level 1 → Level 2 (Generalizations)
        insights = []
        if len(patterns) >= 3:
            insights = trm_compressor.generate_generalizations(patterns, dream_input.user_id)
            
            for i, insight in enumerate(insights):
                insight_id = f"insight_{dream_input.user_id}_{i}"
                bdh_graph.add_insight(
                    insight_id=insight_id,
                    insight=insight["insight"],
                    patterns_used=insight["patterns_used"],
                    score=insight["score"],
                    user_id=dream_input.user_id
                )
            
            user_profile.total_insights = len(insights)
            
            # Step 3: Level 2 → Level 3 (Psychological Profile)
            # Theory of Mind Synthesis
            profile_data = trm_compressor.synthesize_psychological_profile(insights, dream_input.user_id)
            if profile_data:
                bdh_graph.add_psychological_profile(dream_input.user_id, profile_data)
        

        
        # Step 4: Apply Ebbinghaus Decay (Memory Maintenance)
        # Get all Level 0 facts
        all_facts = [
            {"fact_id": f["fact_id"], "stability": f.get("metadata", {}).get("stability", 0.5)} 
            for f in user_facts
        ]
        
        # Simulate 1 day passing for decay calculation
        decayed_facts = trm_compressor.apply_ebbinghaus_decay(all_facts, days_elapsed=1.0)
        
        # Prune fading memories (Conceptual)
        fading_count = sum(1 for f in decayed_facts if f["status"] == "fading")
        
        return {
            "status": "success",
            "summary": f"Processed {len(user_facts)} facts",
            "patterns": [p["pattern"] for p in patterns],
            "insights": [i["insight"] for i in insights],
            "profile_updated": len(insights) > 0,
            "memories_fading": fading_count,
            "graph_stats": bdh_graph.get_stats()
        }
        
    except Exception as e:
        print(f"Error in dream cycle: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/v1/intuitive/predict/{user_id}")
async def get_prediction(user_id: str):
    """
    Active Inference Prediction Endpoint
    Returns a proactive suggestion if the system anticipates a need.
    """
    try:
        user_profile = get_user_profile(user_id)
        
        # Generate prediction based on current state
        prediction = predictive_engine.predict_next_need(user_profile)
        
        if prediction:
            return {
                "status": "suggestion_available",
                "prediction": prediction
            }
        else:
            return {
                "status": "no_suggestion",
                "message": "Free energy is minimized (no surprise anticipated)"
            }
            
    except Exception as e:
        print(f"Error in prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

