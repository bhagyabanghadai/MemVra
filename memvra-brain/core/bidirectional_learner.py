"""
Bidirectional Learner - Feature 6
Learns from HOW users query, not just WHAT
"""
from typing import Dict
from collections import Counter
from core.user_profile import UserProfile


class BidirectionalLearner:
    """Adapts retrieval strategy based on user query patterns"""
    
    def analyze_query_style(self, user_profile: UserProfile):
        """Analyze user's query style and update profile"""
        queries = user_profile.query_patterns
        
        if not queries:
            return
        
        style = {}
        query_texts = [q.get("query", "") for q in queries]
        all_queries = " ".join(query_texts).lower()
        
        # Check for consolidated preference
        if all_queries.count("all") + all_queries.count("summary") > len(queries) * 0.3:
            style["prefers_consolidated"] = True
            style["default_level"] = 2
        else:
            style["prefers_consolidated"] = False
            style["default_level"] = 1
        
        # Check for temporal bias
        if all_queries.count("recent") + all_queries.count("latest") > len(queries) * 0.4:
            style["temporal_bias"] = "recent"
        
        # Check for reasoning preference
        if all_queries.count("why") + all_queries.count("explain") > len(queries) * 0.2:
            style["wants_reasoning"] = True
        
        user_profile.query_style = style
        user_profile.update_last_modified()
    
    def adapt_retrieval_params(self, user_profile: UserProfile) -> Dict:
        """Get retrieval parameters based on learned style"""
        style = user_profile.query_style
        
        return {
            "start_level": style.get("default_level", 2),
            "sort_by": "timestamp" if style.get("temporal_bias") else "relevance",
            "include_explanations": style.get("wants_reasoning", False)
        }
