"""
Example demonstrating semantic graph analysis and network structures.
"""

from pardes import SemanticGraph


def main():
    # Sample text for network analysis
    text = """
    Knowledge connects to wisdom through understanding.
    Wisdom relates to truth through experience.
    Truth links to knowledge through observation.
    Understanding bridges wisdom and knowledge.
    Experience deepens understanding and truth.
    Observation grounds knowledge in reality.
    """
    
    print("=" * 70)
    print("PaRDeS Semantic Graph Example - Sod Layer (Integrative Analysis)")
    print("=" * 70)
    print()
    
    # Build co-occurrence graph
    graph = SemanticGraph()
    graph.build_cooccurrence_graph(text, window_size=5, min_frequency=1)
    
    print("GRAPH STATISTICS:")
    print("-" * 60)
    stats = graph.get_graph_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.4f}")
        else:
            print(f"  {key}: {value}")
    print()
    
    # Find central concepts
    print("CENTRAL CONCEPTS (by degree centrality):")
    print("-" * 60)
    central = graph.get_central_concepts(top_n=8, centrality_type="degree")
    for concept, score in central:
        print(f"  {concept}: {score:.4f}")
    print()
    
    # Alternative centrality measures
    print("CENTRAL CONCEPTS (by betweenness centrality):")
    print("-" * 60)
    betweenness = graph.get_central_concepts(top_n=5, centrality_type="betweenness")
    for concept, score in betweenness:
        print(f"  {concept}: {score:.4f}")
    print()
    
    # Find communities
    print("SEMANTIC COMMUNITIES:")
    print("-" * 60)
    communities = graph.find_communities()
    for i, community in enumerate(communities, 1):
        print(f"  Community {i}: {', '.join(sorted(community)[:8])}")
    print()
    
    # Demonstrate custom graph building
    print("CUSTOM CONCEPT NETWORK:")
    print("-" * 60)
    custom_graph = SemanticGraph()
    
    # Add concepts
    custom_graph.add_concept_node("literal", layer="peshat")
    custom_graph.add_concept_node("symbolic", layer="remez")
    custom_graph.add_concept_node("relational", layer="derash")
    custom_graph.add_concept_node("integrative", layer="sod")
    
    # Add relationships
    custom_graph.add_relationship("literal", "symbolic", "builds_upon")
    custom_graph.add_relationship("symbolic", "relational", "builds_upon")
    custom_graph.add_relationship("relational", "integrative", "builds_upon")
    custom_graph.add_relationship("literal", "integrative", "connects_to")
    
    print("  Created PaRDeS layer network with 4 nodes and relationships")
    
    # Find path
    path = custom_graph.find_shortest_path("literal", "integrative")
    if path:
        print(f"  Path from 'literal' to 'integrative': {' -> '.join(path)}")
    
    # Get neighborhood
    neighborhood = custom_graph.get_neighborhood("symbolic", radius=1)
    print(f"  Neighborhood of 'symbolic': {', '.join(neighborhood)}")
    print()
    
    # Export graph data
    print("EXPORT CAPABILITIES:")
    print("-" * 60)
    export_data = custom_graph.export_graph_data()
    print(f"  Nodes: {len(export_data['nodes'])}")
    print(f"  Edges: {len(export_data['edges'])}")
    print(f"  Data ready for visualization or storage")
    print()


if __name__ == "__main__":
    main()
