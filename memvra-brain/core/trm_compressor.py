"""
TRM Compressor - Hierarchical Compression Engine
Compresses Level 0 → Level 1 → Level 2
"""
from typing import Dict, List
from collections import Counter
import re


class TRMCompressor:
    """
    TinyRecursive Model (TRM) - Hierarchical compression
    - Level 0→1: Observations → Reflections (Insights)
    - Level 1→2: Reflections → Generalizations (Personality)
    - Level 2→3: Generalizations → Psychological Profile (Theory of Mind)
    """
    
    def __init__(self):
        self.facts_per_pattern = 5  # Reduced for faster testing
        self.patterns_per_insight = 3
        
        # SM-2 Algorithm Constants
        self.min_ease_factor = 1.3
        self.initial_interval = 1  # Days
    
    def calculate_memory_score(self, quality: int, previous_ease: float, previous_interval: int) -> Dict:
        """
        Implement SM-2 Algorithm for Spaced Repetition
        Input:
            quality: 0-5 rating of recall quality (5=perfect, 0=forgot)
            previous_ease: Previous Ease Factor (default 2.5)
            previous_interval: Previous interval in days
        Output:
            {new_ease, new_interval, stability_score}
        """
        # 1. Update Ease Factor
        # EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        new_ease = previous_ease + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        new_ease = max(self.min_ease_factor, new_ease)
        
        # 2. Update Interval
        if previous_interval == 0:
            new_interval = 1
        elif previous_interval == 1:
            new_interval = 6
        else:
            new_interval = int(previous_interval * new_ease)
            
        # 3. Calculate Stability (0.0 - 1.0)
        # Higher interval = Higher stability
        stability = min(1.0, new_interval / 30)  # Cap at 1.0 (30 days)
        
        return {
            "ease_factor": new_ease,
            "interval": new_interval,
            "stability": stability
        }

    def apply_ebbinghaus_decay(self, memory_nodes: List[Dict], days_elapsed: float) -> List[Dict]:
        """
        Apply Ebbinghaus Forgetting Curve: R = e^(-t/S)
        - t: Time elapsed (days)
        - S: Stability (Memory Strength)
        """
        import math
        
        decayed_nodes = []
        for node in memory_nodes:
            stability = node.get("stability", 0.5)  # Default stability
            
            # R = e^(-t/S)
            # We use S * 10 to scale it to days (S=1.0 -> 10 days half-life)
            strength = max(0.1, stability * 10)
            retention = math.exp(-days_elapsed / strength)
            
            node["retention"] = retention
            
            # If retention drops below threshold, mark for compression/archival
            if retention < 0.3:
                node["status"] = "fading"
            else:
                node["status"] = "active"
                
            decayed_nodes.append(node)
            
        return decayed_nodes

    
    def generate_reflections(self, facts: List[Dict], user_id: str) -> List[Dict]:
        """
        Level 0 → Level 1: Generate Reflections from Observations
        Uses simple heuristic for now (Keyword Clustering), 
        TODO: Replace with LLM call for true semantic reflection
        """
        return self.compress_level_0_to_1(facts, user_id)

    def generate_generalizations(self, reflections: List[Dict], user_id: str) -> List[Dict]:
        """
        Level 1 → Level 2: Generate Generalizations from Reflections
        """
        return self.compress_level_1_to_2(reflections, user_id)

    def synthesize_psychological_profile(self, generalizations: List[Dict], user_id: str) -> Dict:
        """
        Level 2 → Level 3: Synthesize Psychological Profile (Theory of Mind)
        """
        if not generalizations:
            return {}
            
        # Mock Profile Synthesis (Placeholder for LLM)
        traits = [g["topic"] for g in generalizations]
        
        return {
            "user_id": user_id,
            "traits": list(set(traits)),
            "beliefs": [f"Believes {t} is important" for t in traits],
            "intents": ["Improve productivity", "Learn new things"], # inferred
            "emotions": ["Curious", "Determined"] # inferred
        }
    
    def compress_level_0_to_1(self, facts: List[Dict], user_id: str) -> List[Dict]:
        """
        Compress raw facts into patterns
        Input: 20+ facts
        Output: Patterns with confidence scores
        """
        if len(facts) < 5:
            return []  # Need minimum facts to detect pattern
        
        # Group facts by topic/domain
        grouped = self._group_by_topic(facts)
        
        patterns = []
        for topic, topic_facts in grouped.items():
            if len(topic_facts) >= 3:  # Minimum for pattern
                # Extract pattern
                pattern_text = self._extract_pattern(topic, topic_facts)
                confidence = min(1.0, len(topic_facts) / self.facts_per_pattern)
                
                patterns.append({
                    "pattern": pattern_text,
                    "topic": topic,
                    "facts_compressed": [f["fact_id"] for f in topic_facts],
                    "confidence": confidence,
                    "user_id": user_id
                })
        
        return patterns
    
    def compress_level_1_to_2(self, patterns: List[Dict], user_id: str) -> List[Dict]:
        """
        Compress patterns into meta-insights (personality traits)
        Input: 50+ patterns
        Output: 3-5 meta-insights
        """
        if len(patterns) < 3:
            return []
        
        # Analyze cross-pattern themes
        insights = []
        
        # Extract common themes across patterns
        all_topics = [p["topic"] for p in patterns]
        topic_counts = Counter(all_topics)
        
        # Top 3 topics become insights
        for topic, count in topic_counts.most_common(3):
            insight_text = self._synthesize_insight(topic, count, len(patterns))
            score = count / len(patterns)
            
            insights.append({
                "insight": insight_text,
                "topic": topic,
                "patterns_used": [
                    p.get("pattern_id", i) 
                    for i, p in enumerate(patterns) 
                    if p["topic"] == topic
                ],
                "score": score,
                "user_id": user_id
            })
        
        return insights
    
    def _group_by_topic(self, facts: List[Dict]) -> Dict[str, List[Dict]]:
        """Group facts by detected topic/domain"""
        grouped = {}
        
        # Simple keyword-based grouping
        keywords = {
            "UI": ["ui", "interface", "design", "theme", "dark", "light"],
            "Coding": ["code", "programming", "typescript", "javascript", "python"],
            "Performance": ["performance", "optimize", "speed", "fast", "slow"],
            "Tools": ["tool", "editor", "vscode", "ide"],
            "Preferences": ["prefer", "like", "favorite", "love", "hate"]
        }
        
        for fact in facts:
            content = fact.get("content", "").lower()
            matched_topic = "General"
            
            for topic, topic_keywords in keywords.items():
                if any(kw in content for kw in topic_keywords):
                    matched_topic = topic
                    break
            
            if matched_topic not in grouped:
                grouped[matched_topic] = []
            grouped[matched_topic].append(fact)
        
        return grouped
    
    def _extract_pattern(self, topic: str, facts: List[Dict]) -> str:
        """Extract pattern description from facts"""
        fact_count = len(facts)
        
        # Extract common words
        all_words = " ".join([f.get("content", "") for f in facts]).lower()
        words = re.findall(r'\w+', all_words)
        common_words = [word for word, count in Counter(words).most_common(3) if len(word) > 3]
        
        # Generate pattern description
        pattern = f"{topic}_PREFERENCE → {', '.join(common_words)} (from {fact_count} facts)"
        
        return pattern
    
    def _synthesize_insight(self, topic: str, pattern_count: int, total_patterns: int) -> str:
        """Synthesize meta-insight from patterns"""
        percentage = int((pattern_count / total_patterns) * 100)
        
        insight = f"User shows strong {topic.lower()} focus ({percentage}% of patterns). "
        insight += f"This appears in {pattern_count} distinct patterns."
        
        return insight
    
    def analyze_sentiment(self, facts: List[Dict]) -> str:
        """Simple sentiment analysis"""
        positive_words = ["good", "great", "love", "excellent", "prefer", "like", "best"]
        negative_words = ["bad", "hate", "worst", "dislike", "avoid", "poor"]
        
        pos_count = 0
        neg_count = 0
        
        for fact in facts:
            content = fact.get("content", "").lower()
            pos_count += sum(1 for word in positive_words if word in content)
            neg_count += sum(1 for word in negative_words if word in content)
        
        if pos_count > neg_count * 1.5:
            return "positive"
        elif neg_count > pos_count * 1.5:
            return "negative"
        else:
            return "neutral"
