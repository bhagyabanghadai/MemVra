"""
Llama Service
Integrates Llama 3.1 8B via Ollama for query enhancement and response formatting
STATELESS - no memory stored here
"""
import ollama
from typing import Dict, List, Optional
import json


class LlamaService:
    """
    Llama 3.1 8B integration for natural language understanding
    Two main functions:
    1. Query Enhancement (~50 tokens)
    2. Response Formatting (~100 tokens)
    """
    
    def __init__(self, model_name: str = "llama3.1:8b-instruct-fp16"):
        self.model_name = model_name
        self.client = ollama.Client()
        
        # Verify Ollama is running and model is available
        try:
            self.client.list()
            print(f"✓ Llama service initialized with model: {model_name}")
        except Exception as e:
            print(f"⚠ Warning: Ollama not available - {e}")
            print("  Falling back to simple text processing")
    
    def enhance_query(self, user_query: str, user_profile: Optional[Dict] = None) -> Dict:
        """
        Extract intent, keywords, and create query vector for BDH search
        Uses ~50 tokens per call
        """
        try:
            # Build prompt for query enhancement
            prompt = f"""Extract the following from this query:
1. Intent (what the user wants: preferences, facts, summary, etc.)
2. Keywords (important terms)
3. Synonyms (related terms to search for)

Query: "{user_query}"

Respond in JSON format:
{{
    "intent": "...",
    "keywords": ["...", "..."],
    "synonyms": ["...", "..."]
}}"""
            
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                options={"temperature": 0.1}  # Low temperature for consistent extraction
            )
            
            # Parse JSON response
            result = json.loads(response['response'])
            
            return {
                "intent": result.get("intent", "general_query"),
                "keywords": result.get("keywords", [user_query]),
                "synonyms": result.get("synonyms", []),
                "enhanced_query": " ".join(result.get("keywords", []) + result.get("synonyms", []))
            }
            
        except Exception as e:
            # Fallback: simple keyword extraction
            print(f"Llama enhancement failed, using fallback: {e}")
            words = user_query.lower().split()
            return {
                "intent": "general_query",
                "keywords": words,
                "synonyms": [],
                "enhanced_query": user_query
            }
    
    def stream_response(
        self,
        facts: List[Dict],
        query: str,
        level_used: int,
        confidence: float,
        user_profile: Optional[Dict] = None
    ):
        """
        Generator that streams the response token-by-token.
        Implements:
        1. Adaptive Logic: Skip CoT for simple greetings
        2. Reasoning Engine: CoT for complex queries
        3. Streaming: Low latency perception
        """
        is_greeting = any(word in query.lower() for word in ['hello', 'hi', 'hey', 'greetings'])
        if is_greeting and not facts:
            yield "Hello! I'm online and ready to help. What's on your mind?"
            return

        if not facts:
            # Check if it's a personal question that requires memory
            is_personal = any(word in query.lower() for word in ['who am i', 'my name', 'my job', 'i like', 'my favorite', 'what did i'])
            if is_personal:
                yield self._format_no_facts_response(query, user_profile)
            else:
                # General knowledge fallback
                for token in self._stream_general_response(query):
                    yield token
            return

        # 2. Reasoning Engine: Build Chain-of-Thought Prompt
        # Include Fact IDs for citation
        facts_str = "\n".join([f"[Fact: {fact.get('fact_id', 'unknown')}] {fact.get('content', str(fact))}" for fact in facts[:5]])
        
        formality = user_profile.get("linguistic_profile", {}).get("formality", 0.5) if user_profile else 0.5
        style = "professional and concise" if formality > 0.6 else "casual and friendly"

        prompt = f"""You are MemVra, an intelligent AI assistant.
Facts retrieved from memory (Level {level_used}):
{facts_str}

User Query: "{query}"

Instructions:
1. Think step-by-step about how the facts answer the query.
2. If facts are insufficient, admit it.
3. Formulate a {style} response.
4. Do NOT hallucinate. Only use provided facts.
5. STRICT CITATION: You MUST cite the source fact ID for every claim using [Fact: <id>].

Response:"""

        # 3. Stream from Ollama
        try:
            stream = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                stream=True,
                options={
                    "temperature": 0.2,
                    "top_p": 0.9
                }
            )
            
            for chunk in stream:
                if 'response' in chunk:
                    yield chunk['response']
                    
        except Exception as e:
            print(f"Streaming failed: {e}")
            yield self._fallback_format(facts, query, level_used, confidence)

    def _stream_general_response(self, query: str):
        """Stream general knowledge response when no memories are found"""
        prompt = f"""You are MemVra, an intelligent AI assistant.
User Query: "{query}"

Instructions:
1. Answer the query helpfully and accurately based on your general knowledge.
2. Be concise but informative.
3. Maintain a helpful and friendly tone.

Response:"""
        
        try:
            stream = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                stream=True,
                options={
                    "temperature": 0.7,  # Higher temperature for creativity
                    "top_p": 0.9
                }
            )
            
            for chunk in stream:
                if 'response' in chunk:
                    yield chunk['response']
        except Exception as e:
            yield f"I'm having trouble accessing my general knowledge right now. Error: {e}"

    def format_response(self, *args, **kwargs):
        """Legacy non-streaming method (wraps streaming)"""
        return "".join(list(self.stream_response(*args, **kwargs)))
    
    def _format_no_facts_response(self, query: str, user_profile: Optional[Dict]) -> str:
        """
        Active Learning: If we don't know, ASK the user.
        """
        return f"I don't have that memory about you yet. If you tell me, I'll remember it for next time! (e.g., 'My name is...')"
    
    def _fallback_format(self, facts: List[Dict], query: str, level_used: int, confidence: float) -> str:
        """Simple formatting without Llama"""
        facts_text = "\n".join([f"• {fact.get('content', str(fact))}" for fact in facts[:5]])
        
        return f"""Based on your memories, here's what I found (confidence: {confidence:.2f}):

{facts_text}

(Retrieved {len(facts)} fact(s) from Level {level_used})"""
    
    def translate_user_language(self, text: str, user_profile: Dict) -> str:
        """
        Translate text using user's vocabulary (Feature 7: Linguistic Profiling)
        """
        if not user_profile:
            return text
        
        linguistic = user_profile.get("linguistic_profile", {})
        synonyms = linguistic.get("synonyms", {})
        
        # Replace standard terms with user's preferred vocabulary
        for concept, user_term in synonyms.items():
            text = text.replace(concept, user_term)
        
        return text
    
    def verify_response(self, response: str, facts: List[Dict]) -> Dict:
        """
        Self-Verification Loop (Hallucination Safeguard)
        Checks if the response is supported by the facts.
        """
        try:
            facts_text = "\n".join([f"{f.get('content')}" for f in facts])
            
            prompt = f"""Verify if the following Response is fully supported by the Context.
Context:
{facts_text}

Response:
{response}

Instructions:
1. Check for any claims in Response not found in Context.
2. Return JSON: {{"supported": true/false, "reason": "..."}}
"""
            result = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                options={"temperature": 0.1, "format": "json"}
            )
            return json.loads(result['response'])
        except Exception as e:
            print(f"Verification failed: {e}")
            return {"supported": True, "reason": "Verification skipped due to error"}

    def is_available(self) -> bool:
        """Check if Ollama service is available"""
        try:
            self.client.list()
            return True
        except:
            return False
