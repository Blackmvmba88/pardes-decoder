"""
Comprehensive example integrating all four PaRDeS layers.
"""

from pardes import TextParser, PatternDetector, SemanticGraph


def main():
    # Sample text for comprehensive analysis
    text = """
    The ancient art of interpretation reveals layers beneath the surface.
    Each layer provides insight, and insight leads to understanding.
    Understanding emerges from careful observation and systematic analysis.
    The surface meaning is clear and accessible to all readers.
    Beneath the surface lie patterns that repeat and interconnect.
    These patterns form networks of meaning across the text.
    Networks reveal relationships that are not immediately visible.
    Relationships connect concepts in unexpected ways, creating depth.
    The depth of meaning increases as we integrate multiple perspectives.
    Integration synthesizes all layers into a coherent whole.
    """
    
    print("=" * 70)
    print("PaRDeS Comprehensive Analysis - All Four Layers")
    print("=" * 70)
    print()
    
    # LAYER 1: PESHAT (Literal/Surface)
    print("LAYER 1: PESHAT - Literal/Surface Analysis")
    print("=" * 70)
    parser = TextParser(text)
    stats = parser.get_statistics()
    print(f"Total words: {stats['word_count']}")
    print(f"Unique words: {stats['unique_words']}")
    print(f"Sentences: {stats['sentence_count']}")
    print(f"Avg sentence length: {stats['avg_sentence_length']:.1f} words")
    print()
    
    # LAYER 2: REMEZ (Symbolic/Patterns)
    print("LAYER 2: REMEZ - Symbolic Pattern Analysis")
    print("=" * 70)
    detector = PatternDetector(text)
    
    key_concepts = ["meaning", "layer", "pattern", "understanding"]
    print("Key concept frequencies:")
    for concept in key_concepts:
        matches = detector.find_literal_patterns(concept, case_sensitive=False)
        if matches:
            print(f"  {concept}: {len(matches)} occurrences")
    
    repeated = detector.find_repeated_structures(min_occurrences=2)
    if repeated:
        print(f"\nRepeated structures found: {len(repeated)}")
        for struct in repeated[:3]:
            print(f"  - '{struct['pattern']}'")
    print()
    
    # LAYER 3: DERASH (Relational/Contextual)
    print("LAYER 3: DERASH - Relational Analysis")
    print("=" * 70)
    
    # Analyze co-occurrences
    concept_pairs = [
        ("meaning", "understanding"),
        ("pattern", "network"),
        ("layer", "depth")
    ]
    
    print("Concept relationships (co-occurrences):")
    for w1, w2 in concept_pairs:
        co_occurs = detector.find_co_occurrences(w1, w2, window_size=100)
        if co_occurs:
            print(f"  {w1} <-> {w2}: {len(co_occurs)} co-occurrences")
    print()
    
    # LAYER 4: SOD (Integrative/Network)
    print("LAYER 4: SOD - Integrative Network Analysis")
    print("=" * 70)
    
    # Build semantic network
    graph = SemanticGraph()
    graph.build_cooccurrence_graph(text, window_size=5, min_frequency=2)
    
    graph_stats = graph.get_graph_statistics()
    print(f"Network nodes: {graph_stats['nodes']}")
    print(f"Network edges: {graph_stats['edges']}")
    print(f"Network density: {graph_stats['density']:.4f}")
    print(f"Clustering coefficient: {graph_stats.get('avg_clustering', 0):.4f}")
    
    print("\nMost central concepts:")
    central = graph.get_central_concepts(top_n=5)
    for i, (concept, score) in enumerate(central, 1):
        print(f"  {i}. {concept} (centrality: {score:.4f})")
    
    print("\nSemantic communities:")
    communities = graph.find_communities()
    for i, community in enumerate(communities[:3], 1):
        members = ', '.join(sorted(list(community))[:6])
        print(f"  Community {i}: {members}")
    print()
    
    # SYNTHESIS
    print("SYNTHESIS - Integrated Insights")
    print("=" * 70)
    print("This analysis demonstrates the PaRDeS framework as a computational")
    print("methodology for multi-level text analysis:")
    print()
    print("1. PESHAT: Surface-level statistics reveal text structure")
    print("2. REMEZ: Pattern detection uncovers symbolic repetitions")
    print("3. DERASH: Relational analysis shows concept connections")
    print("4. SOD: Network analysis integrates all layers into unified view")
    print()
    print("The framework enables rigorous, reproducible analysis of textual")
    print("meaning without relying on mystical or theological assumptions.")
    print("=" * 70)


if __name__ == "__main__":
    main()
