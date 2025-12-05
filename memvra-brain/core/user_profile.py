"""
User Profile Model
Stores all personalization data for each user
"""
from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel


class UserProfile(BaseModel):
    """
    Comprehensive user profile that powers all personalization features
    """
    user_id: str
    created_at: datetime = datetime.now()
    last_updated: datetime = datetime.now()
    
    # Feature 2: Cross-Domain Synthesis
    personality_traits: Dict[str, Dict] = {}
    # Example: {"efficiency_oriented": {"score": 0.92, "evidence": [...], "domains": [...]}}
    
    domain_correlations: Dict[str, float] = {}
    # Example: {"UI→coding": 0.85, "coding→leisure": 0.72}
    
    # Feature 3: Predictive Recall
    query_patterns: List[Dict] = []
    # Example: [{"query": "...", "timestamp": ..., "day": 0, "hour": 9}]
    
    behavioral_predictions: List[Dict] = []
    # Example: [{"trigger": "monday_9am", "likely_query": "...", "confidence": 0.87}]
    
    # Feature 4: Confidence Decay & Reinforcement
    fact_access_log: Dict[str, datetime] = {}
    # Example: {"fact_123": datetime(...)}
    
    reinforcement_count: Dict[str, int] = {}
    # Example: {"fact_123": 5}  # Mentioned 5 times
    
    # Feature 6: Bidirectional Learning
    query_style: Dict[str, any] = {}
    # Example: {"prefers_consolidated": True, "temporal_bias": "recent", ...}
    
    response_preferences: Dict[str, any] = {}
    # Example: {"wants_reasoning": True, "detail_level": "patterns"}
    
    retrieval_strategy: str = "start_level_2"
    # Options: "start_level_2", "start_level_1", "start_level_0"
    
    # Feature 7: Linguistic Profiling
    linguistic_profile: Dict[str, any] = {
        "vocabulary": {},
        # Example: {"UI": {"frequency": 27, "meaning": "user_interface"}}
        
        "synonyms": {},
        # Example: {"ui_theme": "dark mode", "performance": "optimize"}
        
        "abbreviations": {},
        # Example: {"UI": "user interface", "perf": "performance"}
        
        "formality": 0.5,  # 0.0 (casual) to 1.0 (formal)
        "verbosity": 0.5,  # 0.0 (concise) to 1.0 (detailed)
        "technical_level": 0.5  # 0.0 (layman) to 1.0 (expert)
    }
    
    # Statistics
    total_facts: int = 0
    total_queries: int = 0
    total_patterns: int = 0
    total_insights: int = 0
    
    class Config:
        arbitrary_types_allowed = True
        
    def update_last_modified(self):
        """Update the last modified timestamp"""
        self.last_updated = datetime.now()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for storage"""
        return self.model_dump()
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'UserProfile':
        """Create from dictionary"""
        return cls(**data)
    
    def increment_fact_count(self):
        """Increment fact counter"""
        self.total_facts += 1
        self.update_last_modified()
    
    def increment_query_count(self):
        """Increment query counter"""
        self.total_queries += 1
        self.update_last_modified()
    
    def get_summary(self) -> Dict:
        """Get summary statistics"""
        return {
            "user_id": self.user_id,
            "total_facts": self.total_facts,
            "total_queries": self.total_queries,
            "total_patterns": self.total_patterns,
            "total_insights": self.total_insights,
            "linguistic_style": {
                "formality": self.linguistic_profile["formality"],
                "verbosity": self.linguistic_profile["verbosity"],
                "technical_level": self.linguistic_profile["technical_level"]
            },
            "top_personality_traits": sorted(
                self.personality_traits.items(),
                key=lambda x: x[1].get("score", 0),
                reverse=True
            )[:3] if self.personality_traits else []
        }
