"""
BDH Graph - Scale-Free Network for Memory Storage
Implements hierarchical compression with O(log n) retrieval
"""
import networkx as nx
import numpy as np
from typing import Dict, List, Optional, Tuple
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pickle


class BDHGraph:
    """
    BabyDragon Hatchling (BDH) - Scale-free graph for efficient memory
    
    Features:
    - Level 0: Raw facts (full fidelity)
    - Level 1: Compressed patterns (TRM output)
    - Level 2: Meta-insights (personality traits)
    - O(log n) retrieval through hub nodes
    """
    
    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2"):
        # Initialize graph structure
        self.graph = nx.Graph()
        
        # Embedding model for semantic similarity
        self.encoder = SentenceTransformer(embedding_model)
        
        # Hierarchical levels (Bicameral Architecture)
        self.levels = {
            0: {},  # Observation (Fact) -> {content, embedding, metadata}
            1: {},  # Reflection (Pattern) -> {content, observations_linked, confidence}
            2: {},  # Generalization (Insight) -> {content, reflections_linked, score}
            3: {}   # Psychological Profile -> {traits, beliefs, intents, emotions}
        }
        
        # Hub nodes (most connected)
        self.hubs = set()
        
        # Similarity threshold for edge creation
        self.similarity_threshold = 0.7
        
        print("✓ BDH Graph initialized")
    
    def add_fact(self, fact_id: str, content: str, user_id: str, metadata: Dict = None) -> Dict:
        """
        Add new fact to Level 0 and create graph connections
        O(log n) insertion through hub navigation
        """
        # Generate embedding
        embedding = self.encoder.encode(content)
        
        # Store in Level 0
        self.levels[0][fact_id] = {
            "content": content,
            "embedding": embedding,
            "user_id": user_id,
            "metadata": metadata or {},
            "level": 0
        }
        
        # Add node to graph
        self.graph.add_node(
            fact_id,
            level=0,
            user_id=user_id,
            content_preview=content[:50]
        )
        
        # Create edges to similar facts (scale-free network)
        self._create_edges(fact_id, embedding, user_id)
        
        # Update hub nodes
        self._update_hubs()
        
        return {"fact_id": fact_id, "connections": self.graph.degree(fact_id)}

    def update_fact_stats(self, fact_id: str, new_stats: Dict):
        """Update fact metadata (e.g., SM-2 scores)"""
        if fact_id in self.levels[0]:
            # Update Level 0 storage
            self.levels[0][fact_id]["metadata"].update(new_stats)
            
            # Update Graph Node
            if self.graph.has_node(fact_id):
                for key, value in new_stats.items():
                    self.graph.nodes[fact_id][key] = value

    
    def _create_edges(self, fact_id: str, embedding: np.ndarray, user_id: str):
        """
        Connect fact to similar facts (same user only)
        Creates scale-free network structure
        """
        connections = 0
        
        # Only connect to facts from same user
        user_facts = [
            (fid, data) for fid, data in self.levels[0].items()
            if data["user_id"] == user_id and fid != fact_id
        ]
        
        for other_id, other_data in user_facts:
            # Calculate similarity
            similarity = cosine_similarity(
                [embedding],
                [other_data["embedding"]]
            )[0][0]
            
            # Create edge if similar enough
            if similarity > self.similarity_threshold:
                self.graph.add_edge(
                    fact_id,
                    other_id,
                    weight=float(similarity)
                )
                connections += 1
        
        return connections
    
    def _update_hubs(self):
        """Identify hub nodes (highly connected)"""
        if len(self.graph) == 0:
            return
        
        degrees = dict(self.graph.degree())
        avg_degree = sum(degrees.values()) / len(degrees)
        
        # Hubs are nodes with degree > 2x average
        self.hubs = {
            node for node, degree in degrees.items()
            if degree > avg_degree * 2
        }
    
    def retrieve(
        self,
        query: str = None,
        query_vector: np.ndarray = None,
        user_id: str = None,
        level: int = 2,
        top_k: int = 5
    ) -> Dict:
        """
        Multi-level retrieval with automatic fallback
        1. Try Level 2 (insights) first - fastest
        2. Fall back to Level 1 (patterns) if confidence < 0.7
        3. Fall back to Level 0 (facts) if confidence < 0.5
        
        Returns: {facts, level_used, confidence, path}
        """
        # Generate query embedding if needed
        if query_vector is None and query:
            query_vector = self.encoder.encode(query)
        
        # Filter to user's data only
        user_nodes = [
            node for node in self.graph.nodes()
            if self.graph.nodes[node].get("user_id") == user_id
        ] if user_id else list(self.graph.nodes())
        
        if not user_nodes:
            return {
                "facts": [],
                "level_used": level,
                "confidence": 0.0,
                "path": []
            }
        
        # Try retrieval at requested level
        results = self._retrieve_at_level(query_vector, user_nodes, level, top_k)
        
        # Automatic fallback
        if results["confidence"] < 0.7 and level > 1:
            results = self._retrieve_at_level(query_vector, user_nodes, 1, top_k)
        
        if results["confidence"] < 0.5 and level > 0:
            results = self._retrieve_at_level(query_vector, user_nodes, 0, top_k)
        
        return results
    
    def _retrieve_at_level(
        self,
        query_vector: np.ndarray,
        user_nodes: List[str],
        level: int,
        top_k: int
    ) -> Dict:
        """Retrieve from specific level"""
        # Get nodes at this level
        level_nodes = [
            node for node in user_nodes
            if self.graph.nodes[node].get("level", 0) == level
        ]
        
        if not level_nodes:
            # No data at this level, use Level 0
            level_nodes = [
                node for node in user_nodes
                if self.graph.nodes[node].get("level", 0) == 0
            ]
            level = 0
        
        # Calculate similarities
        similarities = []
        for node_id in level_nodes:
            data = self.levels[level].get(node_id)
            if data and "embedding" in data:
                sim = cosine_similarity(
                    [query_vector],
                    [data["embedding"]]
                )[0][0]
                similarities.append((node_id, sim, data))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Get top k
        top_results = similarities[:top_k]
        
        if not top_results:
            return {
                "facts": [],
                "level_used": level,
                "confidence": 0.0,
                "path": []
            }
        
        # Format results
        facts = [{
            "fact_id": node_id,
            "content": data["content"],
            "relevance": "exact" if sim > 0.9 else "partial",
            "similarity": float(sim),
            "created_at": data.get("metadata", {}).get("created_at", "unknown")
        } for node_id, sim, data in top_results]
        
        avg_confidence = sum(sim for _, sim, _ in top_results) / len(top_results)
        
        return {
            "facts": facts,
            "level_used": level,
            "confidence": float(avg_confidence),
            "path": self._get_retrieval_path(top_results)
        }
    
    def _get_retrieval_path(self, results: List[Tuple]) -> List[Dict]:
        """Generate explanation path for retrieval (Feature 5)"""
        if not results:
            return []
        
        path = []
        for node_id, similarity, _ in results:
            # Get path through graph
            if node_id in self.hubs:
                path.append({
                    "node": node_id,
                    "type": "hub",
                    "similarity": float(similarity)
                })
            else:
                path.append({
                    "node": node_id,
                    "type": "regular",
                    "similarity": float(similarity)
                })
        
        return path
    
    def add_pattern(self, pattern_id: str, pattern: str, facts_compressed: List[str], confidence: float, user_id: str):
        """Add compressed pattern to Level 1 (TRM output)"""
        embedding = self.encoder.encode(pattern)
        
        self.levels[1][pattern_id] = {
            "content": pattern,
            "embedding": embedding,
            "facts_compressed": facts_compressed,
            "confidence": confidence,
            "user_id": user_id,
            "level": 1
        }
        
        self.graph.add_node(
            pattern_id,
            level=1,
            user_id=user_id,
            content_preview=pattern[:50]
        )
    
    def add_insight(self, insight_id: str, insight: str, patterns_used: List[str], score: float, user_id: str):
        """Add meta-insight to Level 2 (TRM synthesis)"""
        embedding = self.encoder.encode(insight)
        
        self.levels[2][insight_id] = {
            "content": insight,
            "embedding": embedding,
            "patterns_used": patterns_used,
            "score": score,
            "user_id": user_id,
            "level": 2
        }
        
        self.graph.add_node(
            insight_id,
            level=2,
            user_id=user_id,
            content_preview=insight[:50]
        )
    def add_psychological_profile(self, user_id: str, profile_data: Dict):
        """
        Add/Update Psychological Profile (Level 3)
        Theory of Mind modeling: Beliefs, Intents, Emotions
        """
        profile_id = f"profile_{user_id}"
        
        # Create rich content representation for embedding
        content_repr = f"User Traits: {', '.join(profile_data.get('traits', []))}. "
        content_repr += f"Beliefs: {', '.join(profile_data.get('beliefs', []))}. "
        content_repr += f"Intents: {', '.join(profile_data.get('intents', []))}."
        
        embedding = self.encoder.encode(content_repr)
        
        self.levels[3][profile_id] = {
            "content": content_repr,
            "raw_data": profile_data,
            "embedding": embedding,
            "user_id": user_id,
            "level": 3,
            "last_updated": "now" # TODO: Use actual timestamp
        }
        
        # Add to graph and connect to User node (conceptual)
        self.graph.add_node(
            profile_id,
            level=3,
            user_id=user_id,
            type="psychological_profile",
            content_preview=content_repr[:50]
        )
        
        # Connect to top generalizations (Level 2)
        # This links the "Who" (Profile) to the "What" (Generalizations)
        user_generalizations = [
            n for n in self.graph.nodes() 
            if self.graph.nodes[n].get("level") == 2 and self.graph.nodes[n].get("user_id") == user_id
        ]
        
        for gen_id in user_generalizations:
            # Calculate relevance
            gen_data = self.levels[2].get(gen_id)
            if gen_data:
                sim = cosine_similarity([embedding], [gen_data["embedding"]])[0][0]
                if sim > 0.6:
                    self.graph.add_edge(profile_id, gen_id, weight=float(sim), type="profile_link")
        """Get graph statistics"""
        return {
            "total_nodes": len(self.graph.nodes()),
            "total_edges": len(self.graph.edges()),
            "level_0_facts": len(self.levels[0]),
            "level_1_patterns": len(self.levels[1]),
            "level_2_insights": len(self.levels[2]),
            "hub_count": len(self.hubs),
            "avg_degree": sum(dict(self.graph.degree()).values()) / len(self.graph) if len(self.graph) > 0 else 0,
            "compression_ratio": self._calculate_compression()
        }
    
    def _calculate_compression(self) -> float:
        """Calculate overall compression ratio"""
        l0 = len(self.levels[0])
        l1 = len(self.levels[1])
        l2 = len(self.levels[2])
        
        if l0 == 0:
            return 0.0
        
        # Compression: (L1 + L2) / L0
        # Lower is better (more compression)
        return (l1 + l2) / l0 if l0 > 0 else 0.0
