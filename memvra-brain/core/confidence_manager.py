"""
Confidence Manager
Implements dynamic confidence decay and reinforcement (Feature 4)
"""
from typing import Dict, Optional
from datetime import datetime, timedelta
from core.user_profile import UserProfile


class ConfidenceManager:
    """
    Manages fact confidence based on:
    - Time decay (facts weaken if not accessed)
    - Reinforcement (facts strengthen when re-mentioned)
    - Contradictions (facts weaken if contradicted)
    """
    
    def __init__(self):
        self.decay_rate = 0.95  # 5% decay per month
        self.reinforcement_boost = 0.1  # +10% per mention
        self.contradiction_penalty = 0.1  # -10% per contradiction
    
    def calculate_confidence(self, fact_id: str, fact: Dict, user_profile: UserProfile) -> float:
        """
        Calculate current confidence for a fact
        
        Formula:
        confidence = base * time_decay * reinforcement * contradiction_penalty
        """
        base_confidence = 1.0
        
        # DECAY: Time since last access
        days_since_access = self._days_since_access(fact_id, fact, user_profile)
        time_decay = self.decay_rate ** (days_since_access / 30.0)  # 5% per month
        
        # REINFORCEMENT: How many times re-mentioned
        reinforcement_count = user_profile.reinforcement_count.get(fact_id, 1)
        reinforcement_boost = min(
            1.2,  # Cap at +20%
            1.0 + (reinforcement_count - 1) * self.reinforcement_boost
        )
        
        # CONTRADICTION: Conflicting facts reduce confidence
        contradictions = self._find_contradictions(fact, user_profile)
        contradiction_penalty = self.decay_rate ** len(contradictions)  # -5% per contradiction
        
        # Calculate final confidence
        final_confidence = base_confidence * time_decay * reinforcement_boost * contradiction_penalty
        
        # Clamp between 0.1 and 1.0
        return max(0.1, min(1.0, final_confidence))
    
    def _days_since_access(self, fact_id: str, fact: Dict, user_profile: UserProfile) -> int:
        """Calculate days since last access"""
        last_access = user_profile.fact_access_log.get(fact_id)
        
        if last_access:
            return (datetime.now() - last_access).days
        else:
            # Never accessed, use creation date
            created_at = fact.get("metadata", {}).get("created_at")
            if isinstance(created_at, str):
                created_at = datetime.fromisoformat(created_at)
            if created_at:
                return (datetime.now() - created_at).days
            return 0
    
    def _find_contradictions(self, fact: Dict, user_profile: UserProfile) -> list:
        """Find facts that contradict this one (simplified)"""
        # TODO: Implement semantic contradiction detection
        # For now, return empty list
        return []
    
    def on_fact_accessed(self, fact_id: str, user_profile: UserProfile):
        """Update access log when fact is retrieved"""
        user_profile.fact_access_log[fact_id] = datetime.now()
        user_profile.update_last_modified()
    
    def on_fact_restated(self, fact_id: str, user_profile: UserProfile):
        """Increment reinforcement when fact is re-mentioned"""
        current_count = user_profile.reinforcement_count.get(fact_id, 1)
        user_profile.reinforcement_count[fact_id] = current_count + 1
        user_profile.update_last_modified()
    
    def get_low_confidence_facts(self, user_profile: UserProfile, threshold: float = 0.5) -> list:
        """Get facts with confidence below threshold (for verification prompts)"""
        low_confidence = []
        
        # Check all facts for this user
        # TODO: Integrate with BDH graph to get user's facts
        
        return low_confidence
    
    def prompt_verification(self, fact: Dict, confidence: float, user_profile: UserProfile) -> Optional[str]:
        """Generate verification prompt for low-confidence facts"""
        if confidence >= 0.5:
            return None
        
        fact_content = fact.get("content", "")
        days_old = self._days_since_access(fact.get("fact_id", ""), fact, user_profile)
        
        if days_old > 180:  # 6 months
            return f"You mentioned '{fact_content}' {days_old} days ago but haven't referenced it since. Is this still accurate?"
        
        return None
