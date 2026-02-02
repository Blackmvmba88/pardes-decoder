"""
Semantic Graph Module - Sod Layer (Integrative/Network Analysis)

Provides graph-based semantic structures for integrative text analysis.
This represents the "S" (Sod) level - integrated semantic network analysis
showing relationships and connections between concepts.
"""

import networkx as nx
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict
from pardes.text_parser import TextParser


class SemanticGraph:
    """
    Graph-based representation of semantic relationships in text.
    
    Builds and analyzes semantic networks showing:
    - Word co-occurrence networks
    - Concept relationship graphs
    - Semantic clustering
    - Centrality and importance measures
    """
    
    def __init__(self):
        """Initialize an empty semantic graph."""
        self.graph = nx.Graph()
        self._parser = TextParser()
    
    def build_cooccurrence_graph(self, text: str, window_size: int = 5,
                                 min_frequency: int = 2,
                                 lowercase: bool = True) -> None:
        """
        Build a graph based on word co-occurrence within a sliding window.
        
        Args:
            text: Input text to analyze
            window_size: Size of the sliding window (in words)
            min_frequency: Minimum co-occurrence frequency to include edge
            lowercase: Whether to normalize words to lowercase
        """
        self._parser.load_text(text)
        words = self._parser.tokenize_words(lowercase=lowercase)
        
        # Count co-occurrences
        co_occurrence = defaultdict(int)
        
        for i in range(len(words)):
            window = words[i:i+window_size]
            # Add edges for all pairs in the window
            for j in range(len(window)):
                for k in range(j+1, len(window)):
                    pair = tuple(sorted([window[j], window[k]]))
                    co_occurrence[pair] += 1
        
        # Build graph
        self.graph.clear()
        for (word1, word2), count in co_occurrence.items():
            if count >= min_frequency:
                if self.graph.has_edge(word1, word2):
                    self.graph[word1][word2]['weight'] += count
                else:
                    self.graph.add_edge(word1, word2, weight=count)
    
    def build_sentence_graph(self, text: str, min_common_words: int = 2) -> None:
        """
        Build a graph where nodes are sentences and edges connect similar sentences.
        
        Args:
            text: Input text to analyze
            min_common_words: Minimum number of common words for an edge
        """
        self._parser.load_text(text)
        sentences = self._parser.segment_sentences()
        
        # Create sentence nodes with word sets
        sentence_words = []
        for i, sent in enumerate(sentences):
            self._parser.load_text(sent)
            words = set(self._parser.tokenize_words(lowercase=True))
            label = sent[:50] + ('...' if len(sent) > 50 else '')
            sentence_words.append((i, label, words))
        
        # Build graph
        self.graph.clear()
        for i, label_i, words_i in sentence_words:
            self.graph.add_node(i, label=label_i, word_count=len(words_i))
        
        # Add edges for similar sentences
        for i, label_i, words_i in sentence_words:
            for j, label_j, words_j in sentence_words[i+1:]:
                common = words_i & words_j
                if len(common) >= min_common_words:
                    similarity = len(common) / max(len(words_i), len(words_j))
                    self.graph.add_edge(i, j, weight=similarity, common_words=len(common))
        
        # Restore original text
        self._parser.load_text(text)
    
    def add_concept_node(self, concept: str, **attributes) -> None:
        """
        Add a concept node to the graph.
        
        Args:
            concept: The concept name
            **attributes: Additional node attributes
        """
        self.graph.add_node(concept, **attributes)
    
    def add_relationship(self, concept1: str, concept2: str, 
                        relationship_type: str = "related",
                        weight: float = 1.0, **attributes) -> None:
        """
        Add a relationship (edge) between two concepts.
        
        Args:
            concept1: First concept
            concept2: Second concept
            relationship_type: Type of relationship
            weight: Strength of relationship
            **attributes: Additional edge attributes
        """
        self.graph.add_edge(concept1, concept2, 
                          relationship=relationship_type,
                          weight=weight,
                          **attributes)
    
    def get_central_concepts(self, top_n: int = 10, 
                            centrality_type: str = "degree") -> List[Tuple[str, float]]:
        """
        Get the most central concepts in the graph.
        
        Args:
            top_n: Number of top concepts to return
            centrality_type: Type of centrality ("degree", "betweenness", "closeness", "eigenvector")
            
        Returns:
            List of (concept, centrality_score) tuples
        """
        if len(self.graph) == 0:
            return []
        
        if centrality_type == "degree":
            centrality = nx.degree_centrality(self.graph)
        elif centrality_type == "betweenness":
            centrality = nx.betweenness_centrality(self.graph)
        elif centrality_type == "closeness":
            centrality = nx.closeness_centrality(self.graph)
        elif centrality_type == "eigenvector":
            try:
                centrality = nx.eigenvector_centrality(self.graph, max_iter=1000)
            except nx.PowerIterationFailedConvergence:
                # Fallback to degree centrality if eigenvector doesn't converge
                centrality = nx.degree_centrality(self.graph)
        else:
            raise ValueError(f"Unknown centrality type: {centrality_type}")
        
        sorted_concepts = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
        return sorted_concepts[:top_n]
    
    def find_communities(self) -> List[Set]:
        """
        Detect communities (clusters) in the graph.
        
        Returns:
            List of sets, each containing nodes in a community
        """
        if len(self.graph) == 0:
            return []
        
        # Use greedy modularity communities
        communities = nx.community.greedy_modularity_communities(self.graph)
        return [set(c) for c in communities]
    
    def find_shortest_path(self, concept1: str, concept2: str) -> Optional[List[str]]:
        """
        Find the shortest path between two concepts.
        
        Args:
            concept1: Starting concept
            concept2: Ending concept
            
        Returns:
            List of concepts forming the path, or None if no path exists
        """
        try:
            return nx.shortest_path(self.graph, concept1, concept2)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None
    
    def get_neighborhood(self, concept: str, radius: int = 1) -> Set[str]:
        """
        Get all concepts within a given radius of a concept.
        
        Args:
            concept: The central concept
            radius: How many hops to include
            
        Returns:
            Set of concepts in the neighborhood
        """
        if concept not in self.graph:
            return set()
        
        neighborhood = {concept}
        current_level = {concept}
        
        for _ in range(radius):
            next_level = set()
            for node in current_level:
                next_level.update(self.graph.neighbors(node))
            neighborhood.update(next_level)
            current_level = next_level
        
        return neighborhood
    
    def get_graph_statistics(self) -> Dict:
        """
        Get statistical measures of the graph.
        
        Returns:
            Dictionary with graph statistics
        """
        if len(self.graph) == 0:
            return {
                'nodes': 0,
                'edges': 0,
                'density': 0,
                'connected_components': 0,
            }
        
        stats = {
            'nodes': self.graph.number_of_nodes(),
            'edges': self.graph.number_of_edges(),
            'density': nx.density(self.graph),
            'connected_components': nx.number_connected_components(self.graph),
        }
        
        # Add average clustering coefficient if graph is not empty
        if stats['nodes'] > 0:
            stats['avg_clustering'] = nx.average_clustering(self.graph)
        
        # Add diameter if graph is connected
        if stats['connected_components'] == 1:
            stats['diameter'] = nx.diameter(self.graph)
            stats['avg_shortest_path'] = nx.average_shortest_path_length(self.graph)
        
        return stats
    
    def export_graph_data(self) -> Dict:
        """
        Export graph data for visualization or storage.
        
        Returns:
            Dictionary with nodes and edges data
        """
        nodes = []
        for node in self.graph.nodes(data=True):
            node_data = {'id': node[0]}
            node_data.update(node[1])
            nodes.append(node_data)
        
        edges = []
        for edge in self.graph.edges(data=True):
            edge_data = {
                'source': edge[0],
                'target': edge[1]
            }
            edge_data.update(edge[2])
            edges.append(edge_data)
        
        return {
            'nodes': nodes,
            'edges': edges,
            'statistics': self.get_graph_statistics()
        }
    
    def clear(self) -> None:
        """Clear the graph."""
        self.graph.clear()
