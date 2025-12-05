"""
Predictive Engine - Active Inference & Free Energy Principle
Feature 3: The "Intuition"
"""
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import math
from core.user_profile import UserProfile

class PredictiveEngine:
    """
    Bicameral Predictive Brain
    Uses Active Inference to minimize 'Surprise' (Free Energy)
    """
    
    def __init__(self):
        self.surprise_threshold = 0.3  # Threshold to trigger a suggestion
        self.learning_rate = 0.1
    
    def record_query_pattern(self, user_id: str, query: str, timestamp: datetime, user_profile: UserProfile):
        """
        Observation Step: Record sensory input (query)
        This updates the internal state for future predictions.
        """
        # Simple temporal pattern recording
        hour = timestamp.hour
        day = timestamp.weekday()
        
        # Add to short-term context
        if not hasattr(user_profile, "context_window"):
            user_profile.context_window = []
            
        user_profile.context_window.append({
            "query": query,
            "hour": hour,
            "day": day,
            "timestamp": timestamp.isoformat()
        })
        
        # Keep context window small (last 10 interactions)
        if len(user_profile.context_window) > 10:
            user_profile.context_window.pop(0)

    def predict_next_need(self, user_profile: UserProfile) -> Optional[Dict]:
        """
        Prediction Step: Generate 'Proprioceptive' Prediction
        Based on Theory of Mind (Beliefs/Intents) and Temporal Context.
        
        Returns:
            {
                "suggested_action": str,
                "confidence": float,
                "reasoning": str
            }
        """
        # 1. Get Current Context (Sensory State)
        if not hasattr(user_profile, "context_window") or not user_profile.context_window:
            return None
            
        last_interaction = user_profile.context_window[-1]
        current_hour = datetime.now().hour
        
        # 2. Get Internal Model (Psychological Profile - L3)
        # In a real implementation, this would query the Graph DB for 'PsychologicalProfile'
        # For now, we use the cached profile in the object
        intents = getattr(user_profile, "intents", [])
        traits = getattr(user_profile, "traits", [])
        
        # 3. Active Inference Logic (Simplified)
        # We look for a 'Gap' between Expected State (Goal) and Current State
        
        prediction = None
        
        # Example Logic: "Productivity" Trait + Morning = Need Focus
        if "Productivity" in traits and 8 <= current_hour <= 10:
            prediction = {
                "suggested_action": "Enable Focus Mode",
                "confidence": 0.85,
                "reasoning": "User values productivity and it is morning work hours."
            }
            
        # Example Logic: "Learning" Intent + Question about Code = Need Documentation
        elif any("learn" in i.lower() for i in intents) and "code" in last_interaction["query"].lower():
            prediction = {
                "suggested_action": "Search Official Documentation",
                "confidence": 0.9,
                "reasoning": "User has learning intent and is asking about code."
            }
            
        # 4. Safety Check (Human-in-the-Loop)
        # Only return if confidence is high enough
        if prediction and prediction["confidence"] > self.surprise_threshold:
            return prediction
            
        return None

    def minimize_surprise(self, user_id: str, prediction: Dict, user_feedback: bool):
        """
        Learning Step: Update Internal Model to minimize future surprise.
        - If feedback is Positive (True): Reinforce model (Lower Free Energy).
        - If feedback is Negative (False): Update model (High Prediction Error).
        """
        # In a real system, this would update weights in a Bayesian Network
        # Here we just log the 'Surprise' (Prediction Error)
        
        if user_feedback:
            # Prediction was correct -> Low Surprise
            # Reinforce the pattern (e.g., increase confidence for next time)
            pass 
        else:
            # Prediction was wrong -> High Surprise
            # We must update our internal model (e.g., "User does NOT want coffee at 8 PM")
            pass

