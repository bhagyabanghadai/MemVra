"""
Linguistic Profiler - Feature 7
Learns each user's unique vocabulary and communication style
"""
from typing import Dict, List
from collections import Counter
import re
from core.user_profile import UserProfile


class LinguisticProfiler:
    """
    Learns how each user communicates:
    - Vocabulary (unique words)
    - Abbreviations (shortcuts)
    - Synonyms (how they express concepts)
    - Style (formality, verbosity, technical level)
    """
    
    def __init__(self):
        pass
    
    def build_profile(self, user_data: List[str], user_profile: UserProfile):
        """
        Analyze all user content and build linguistic profile
        user_data: List of all facts and queries from user
        """
        if not user_data:
            return
        
        # Extract vocabulary
        vocabulary = self._extract_vocabulary(user_data)
        user_profile.linguistic_profile["vocabulary"] = vocabulary
        
        # Detect abbreviations
        abbrevs = self._detect_abbreviations(user_data)
        user_profile.linguistic_profile["abbreviations"] = abbrevs
        
        # Detect synonyms/preferences
        synonyms = self._detect_synonym_patterns(user_data)
        user_profile.linguistic_profile["synonyms"] = synonyms
        
        # Analyze communication style
        user_profile.linguistic_profile["formality"] = self._measure_formality(user_data)
        user_profile.linguistic_profile["verbosity"] = self._measure_verbosity(user_data)
        user_profile.linguistic_profile["technical_level"] = self._measure_technical_level(user_data)
        
        user_profile.update_last_modified()
    
    def _extract_vocabulary(self, user_data: List[str]) -> Dict:
        """Find user-specific words they use frequently"""
        all_text = " ".join(user_data).lower()
        words = re.findall(r'\b\w+\b', all_text)
        word_freq = Counter(words)
        
        # Keep words used 3+ times and longer than 2 chars
        vocabulary = {}
        for word, count in word_freq.items():
            if count >= 3 and len(word) > 2:
                vocabulary[word] = {
                    "frequency": count,
                    "meaning": word  # Could be enhanced with semantic analysis
                }
        
        return vocabulary
    
    def _detect_abbreviations(self, user_data: List[str]) -> Dict:
        """Detect common abbreviations"""
        common_abbrevs = {
            "UI": "user interface",
            "UX": "user experience",
            "perf": "performance",
            "TS": "TypeScript",
            "JS": "JavaScript",
            "API": "application programming interface",
            "DB": "database"
        }
        
        detected = {}
        all_text = " ".join(user_data)
        
        for abbrev, full in common_abbrevs.items():
            if abbrev in all_text:
                detected[abbrev] = full
        
        return detected
    
    def _detect_synonym_patterns(self, user_data: List[str]) -> Dict:
        """Learn how user expresses common concepts"""
        synonyms = {}
        all_text = " ".join(user_data).lower()
        
        # Check which  term they prefer for common concepts
        if "dark mode" in all_text and "night mode" not in all_text:
            synonyms["ui_theme"] = "dark mode"
        elif "night mode" in all_text:
            synonyms["ui_theme"] = "night mode"
        
        if all_text.count("optimize") > all_text.count("improve"):
            synonyms["performance_action"] = "optimize"
        else:
            synonyms["performance_action"] = "improve"
        
        return synonyms
    
    def _measure_formality(self, user_data: List[str]) -> float:
        """Measure formality (0.0 = casual, 1.0 = formal)"""
        all_text = " ".join(user_data).lower()
        
        # Casual indicators
        casual_indicators = ["lol", "btw", "gonna", "wanna", "yeah", "nah"]
        casual_count = sum(text.count(ind) for ind in casual_indicators for text in user_data)
        
        # Formal indicators
        formal_indicators = ["however", "therefore", "furthermore", "regarding"]
        formal_count = sum(text.count(ind) for ind in formal_indicators for text in user_data)
        
        # Contractions suggest casual
        contractions = len(re.findall(r"\w+n't|\w+'s|\w+'re", all_text))
        
        # Calculate formality score
        if casual_count + contractions > formal_count * 2:
            return 0.3  # Casual
        elif formal_count > casual_count * 2:
            return 0.8  # Formal
        else:
            return 0.5  # Neutral
    
    def _measure_verbosity(self, user_data: List[str]) -> float:
        """Measure verbosity (0.0 = concise, 1.0 = detailed)"""
        if not user_data:
            return 0.5
        
        avg_length = sum(len(text.split()) for text in user_data) / len(user_data)
        
        # < 5 words = concise, > 20 words = verbose
        if avg_length < 5:
            return 0.2
        elif avg_length > 20:
            return 0.8
        else:
            return (avg_length - 5) / 15  # Scale between 5-20 words
    
    def _measure_technical_level(self, user_data: List[str]) -> float:
        """Measure technical level (0.0 = layman, 1.0 = expert)"""
        all_text = " ".join(user_data).lower()
        
        technical_terms = [
            "api", "database", "algorithm", "optimization", "refactor",
            "async", "await", "typescript", "python", "react", "component",
            "state", "props", "hook", "closure", "prototype"
        ]
        
        tech_count = sum(all_text.count(term) for term in technical_terms)
        words_count = len(all_text.split())
        
        if words_count == 0:
            return 0.5
        
        # Tech terms ratio
        ratio = tech_count / words_count
        
        return min(1.0, ratio * 50)  # Scale up to reasonable level
    
    def adapt_response(self, response: str, user_profile: UserProfile) -> str:
        """Adapt response to match user's communication style"""
        linguistic = user_profile.linguistic_profile
        
        # Translate to user's preferred terms
        for concept, user_term in linguistic.get("synonyms", {}).items():
            # Replace standard term with user's preference
            response = response.replace(concept, user_term)
        
        # Adjust formality
        if linguistic.get("formality", 0.5) < 0.4:
            # Make more casual
            response = response.replace("However,", "But")
            response = response.replace("Therefore,", "So")
        
        # Adjust verbosity
        if linguistic.get("verbosity", 0.5) < 0.3:
            # Make more concise - remove filler phrases
            response = response.replace("Based on your memories, ", "")
            response = response.replace("It appears that ", "")
        
        return response
    
    def understand_query(self, query: str, user_profile: UserProfile) -> str:
        """Translate user's query to standardized form"""
        linguistic = user_profile.linguistic_profile
        
        # Expand abbreviations
        for abbrev, full in linguistic.get("abbreviations", {}).items():
            query = query.replace(abbrev, full)
        
        # Map synonyms to standard concepts
        for concept, user_term in linguistic.get("synonyms", {}).items():
            query = query.replace(user_term, concept)
        
        return query
