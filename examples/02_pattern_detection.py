"""
Example demonstrating pattern detection at multiple levels.
"""

from pardes import PatternDetector


def main():
    # Sample text with deliberate patterns
    text = """
    In the beginning was the pattern, and the pattern was with structure.
    The pattern repeats throughout the text, creating layers of meaning.
    We find patterns in words, patterns in phrases, and patterns in ideas.
    The structure reveals itself through careful analysis and observation.
    Through analysis we discover connections, and through connections we find truth.
    The truth emerges from the pattern, just as the pattern emerges from the structure.
    """
    
    print("=" * 70)
    print("PaRDeS Pattern Detector Example - Remez & Derash Layers")
    print("(Symbolic and Relational Analysis)")
    print("=" * 70)
    print()
    
    # Initialize detector
    detector = PatternDetector(text)
    
    # Find literal patterns
    print("LITERAL PATTERN OCCURRENCES:")
    print("-" * 60)
    keywords = ["pattern", "structure", "analysis"]
    for keyword in keywords:
        matches = detector.find_literal_patterns(keyword, case_sensitive=False)
        print(f"  '{keyword}' appears {len(matches)} times")
    print()
    
    # Find repeated structures
    print("REPEATED STRUCTURAL PATTERNS:")
    print("-" * 60)
    structures = detector.find_repeated_structures(min_occurrences=2)
    for struct in structures[:5]:
        print(f"  '{struct['pattern']}' (occurs {struct['occurrences']} times)")
    print()
    
    # Find co-occurrences
    print("CO-OCCURRENCE ANALYSIS:")
    print("-" * 60)
    word_pairs = [("pattern", "structure"), ("analysis", "truth")]
    for w1, w2 in word_pairs:
        co_occurs = detector.find_co_occurrences(w1, w2, window_size=100)
        print(f"  '{w1}' and '{w2}' co-occur {len(co_occurs)} times")
    print()
    
    # Keyword contexts
    print("CONTEXTUAL ANALYSIS - 'pattern':")
    print("-" * 60)
    contexts = detector.get_keyword_contexts("pattern", context_size=50)
    for i, context in enumerate(contexts[:3], 1):
        print(f"  Context {i}: ...{context.strip()}...")
    print()
    
    # Pattern density
    print("PATTERN DENSITY ANALYSIS:")
    print("-" * 60)
    density = detector.analyze_pattern_density("pattern", segment_size=100)
    for i, segment in enumerate(density, 1):
        if segment['matches'] > 0:
            print(f"  Segment {i}: {segment['matches']} matches "
                  f"(density: {segment['density']:.4f})")
    print()


if __name__ == "__main__":
    main()
