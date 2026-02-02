"""Tests for the semantic_graph module."""

import pytest
from pardes.semantic_graph import SemanticGraph


class TestSemanticGraph:
    """Test suite for SemanticGraph class."""
    
    def test_initialization(self):
        """Test graph initialization."""
        graph = SemanticGraph()
        assert graph.graph.number_of_nodes() == 0
        assert graph.graph.number_of_edges() == 0
    
    def test_build_cooccurrence_graph(self):
        """Test co-occurrence graph building."""
        text = "the cat and the dog played together"
        graph = SemanticGraph()
        graph.build_cooccurrence_graph(text, window_size=3, min_frequency=1)
        
        assert graph.graph.number_of_nodes() > 0
        assert graph.graph.number_of_edges() > 0
    
    def test_build_sentence_graph(self):
        """Test sentence similarity graph building."""
        text = "The cat sat. The dog sat. The bird flew."
        graph = SemanticGraph()
        graph.build_sentence_graph(text, min_common_words=1)
        
        assert graph.graph.number_of_nodes() == 3  # Three sentences
    
    def test_add_concept_node(self):
        """Test adding concept nodes."""
        graph = SemanticGraph()
        graph.add_concept_node("concept1", type="abstract")
        graph.add_concept_node("concept2", type="concrete")
        
        assert graph.graph.number_of_nodes() == 2
        assert "concept1" in graph.graph.nodes()
        assert "concept2" in graph.graph.nodes()
    
    def test_add_relationship(self):
        """Test adding relationships between concepts."""
        graph = SemanticGraph()
        graph.add_concept_node("cat")
        graph.add_concept_node("animal")
        graph.add_relationship("cat", "animal", relationship_type="is_a")
        
        assert graph.graph.has_edge("cat", "animal")
        edge_data = graph.graph["cat"]["animal"]
        assert edge_data["relationship"] == "is_a"
    
    def test_get_central_concepts(self):
        """Test centrality calculation."""
        graph = SemanticGraph()
        
        # Create a simple graph
        graph.add_concept_node("central")
        graph.add_concept_node("node1")
        graph.add_concept_node("node2")
        graph.add_concept_node("node3")
        
        graph.add_relationship("central", "node1")
        graph.add_relationship("central", "node2")
        graph.add_relationship("central", "node3")
        
        central = graph.get_central_concepts(top_n=1, centrality_type="degree")
        assert len(central) > 0
        assert central[0][0] == "central"  # Most central node
    
    def test_find_communities(self):
        """Test community detection."""
        graph = SemanticGraph()
        
        # Create two separate clusters
        graph.add_concept_node("a1")
        graph.add_concept_node("a2")
        graph.add_relationship("a1", "a2")
        
        graph.add_concept_node("b1")
        graph.add_concept_node("b2")
        graph.add_relationship("b1", "b2")
        
        communities = graph.find_communities()
        assert len(communities) >= 1
    
    def test_find_shortest_path(self):
        """Test shortest path finding."""
        graph = SemanticGraph()
        
        graph.add_concept_node("a")
        graph.add_concept_node("b")
        graph.add_concept_node("c")
        
        graph.add_relationship("a", "b")
        graph.add_relationship("b", "c")
        
        path = graph.find_shortest_path("a", "c")
        assert path == ["a", "b", "c"]
    
    def test_find_shortest_path_no_path(self):
        """Test shortest path when no path exists."""
        graph = SemanticGraph()
        
        graph.add_concept_node("a")
        graph.add_concept_node("b")
        # No edge between a and b
        
        path = graph.find_shortest_path("a", "b")
        assert path is None
    
    def test_get_neighborhood(self):
        """Test neighborhood extraction."""
        graph = SemanticGraph()
        
        graph.add_concept_node("center")
        graph.add_concept_node("near1")
        graph.add_concept_node("near2")
        graph.add_concept_node("far")
        
        graph.add_relationship("center", "near1")
        graph.add_relationship("center", "near2")
        graph.add_relationship("near1", "far")
        
        neighborhood = graph.get_neighborhood("center", radius=1)
        assert "center" in neighborhood
        assert "near1" in neighborhood
        assert "near2" in neighborhood
        
        neighborhood_2 = graph.get_neighborhood("center", radius=2)
        assert "far" in neighborhood_2
    
    def test_get_graph_statistics(self):
        """Test graph statistics calculation."""
        graph = SemanticGraph()
        
        graph.add_concept_node("a")
        graph.add_concept_node("b")
        graph.add_relationship("a", "b")
        
        stats = graph.get_graph_statistics()
        assert stats["nodes"] == 2
        assert stats["edges"] == 1
        assert "density" in stats
        assert "connected_components" in stats
    
    def test_export_graph_data(self):
        """Test graph data export."""
        graph = SemanticGraph()
        
        graph.add_concept_node("node1", type="test")
        graph.add_concept_node("node2", type="test")
        graph.add_relationship("node1", "node2", weight=1.5)
        
        data = graph.export_graph_data()
        assert "nodes" in data
        assert "edges" in data
        assert "statistics" in data
        assert len(data["nodes"]) == 2
        assert len(data["edges"]) == 1
    
    def test_clear(self):
        """Test graph clearing."""
        graph = SemanticGraph()
        graph.add_concept_node("test")
        assert graph.graph.number_of_nodes() == 1
        
        graph.clear()
        assert graph.graph.number_of_nodes() == 0
    
    def test_empty_graph_statistics(self):
        """Test statistics on empty graph."""
        graph = SemanticGraph()
        stats = graph.get_graph_statistics()
        
        assert stats["nodes"] == 0
        assert stats["edges"] == 0
