"""
Basic example demonstrating text parsing capabilities.
"""

from pardes import TextParser


def main():
    # Sample text for analysis
    text = """
    The computational analysis of text reveals patterns at multiple levels.
    First, we examine the literal structure. The words themselves carry meaning.
    Second, we look for symbolic patterns. Repeated phrases suggest emphasis.
    Third, we analyze relationships. Words that co-occur form semantic networks.
    Finally, we integrate these layers. The full picture emerges from connections.
    """
    
    print("=" * 60)
    print("PaRDeS Text Parser Example - Peshat Layer (Literal Analysis)")
    print("=" * 60)
    print()
    
    # Initialize parser
    parser = TextParser(text)
    
    # Get basic statistics
    print("TEXT STATISTICS:")
    print("-" * 40)
    stats = parser.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value:.2f}" if isinstance(value, float) else f"  {key}: {value}")
    print()
    
    # Segment sentences
    print("SENTENCES:")
    print("-" * 40)
    sentences = parser.segment_sentences()
    for i, sent in enumerate(sentences, 1):
        print(f"  {i}. {sent.strip()}")
    print()
    
    # Word frequency
    print("TOP 10 WORDS BY FREQUENCY:")
    print("-" * 40)
    word_freq = parser.get_word_frequency(lowercase=True, min_length=3)
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    for word, count in sorted_words:
        print(f"  {word}: {count}")
    print()
    
    # Find repeated phrases
    print("REPEATED PHRASES:")
    print("-" * 40)
    phrases = parser.find_phrases(min_words=2, min_frequency=2)
    if phrases:
        for phrase, count in phrases[:5]:
            print(f"  '{phrase}' appears {count} times")
    else:
        print("  No repeated phrases found")
    print()


if __name__ == "__main__":
    main()
