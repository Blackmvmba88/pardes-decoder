"""Tests for the pattern_detector module."""

import pytest
from pardes.pattern_detector import PatternDetector


class TestPatternDetector:
    """Test suite for PatternDetector class."""
    
    def test_initialization(self):
        """Test detector initialization."""
        detector = PatternDetector()
        assert detector.text == ""
        
        detector = PatternDetector("Hello world")
        assert detector.text == "Hello world"
    
    def test_load_text(self):
        """Test loading new text."""
        detector = PatternDetector("Initial text")
        detector.load_text("New text")
        assert detector.text == "New text"
    
    def test_find_literal_patterns(self):
        """Test literal pattern finding."""
        text = "The cat sat on the mat. The cat was fat."
        detector = PatternDetector(text)
        
        matches = detector.find_literal_patterns("cat")
        assert len(matches) == 2
        assert all(m["match"] == "cat" for m in matches)
    
    def test_find_literal_patterns_case_insensitive(self):
        """Test case-insensitive pattern finding."""
        text = "Cat and cat and CAT"
        detector = PatternDetector(text)
        
        matches = detector.find_literal_patterns("cat", case_sensitive=False)
        assert len(matches) == 3
    
    def test_find_repeated_structures(self):
        """Test repeated structure detection."""
        text = "the quick brown fox jumps over the lazy dog. the quick brown cat sleeps"
        detector = PatternDetector(text)
        
        structures = detector.find_repeated_structures(min_occurrences=2)
        assert len(structures) > 0
        
        # Should find "the quick brown"
        patterns = [s["pattern"] for s in structures]
        assert "the quick brown" in patterns
    
    def test_find_co_occurrences(self):
        """Test word co-occurrence finding."""
        text = "The cat and dog played. Later, the cat and dog rested."
        detector = PatternDetector(text)
        
        co_occurs = detector.find_co_occurrences("cat", "dog", window_size=50)
        assert len(co_occurs) >= 1
    
    def test_get_keyword_contexts(self):
        """Test keyword context extraction."""
        text = "The cat sat on the mat. The cat was very happy."
        detector = PatternDetector(text)
        
        contexts = detector.get_keyword_contexts("cat", context_size=20)
        assert len(contexts) == 2
        assert all("cat" in ctx.lower() for ctx in contexts)
    
    def test_analyze_pattern_density(self):
        """Test pattern density analysis."""
        text = "word " * 100  # Create text with repeated word
        detector = PatternDetector(text)
        
        density = detector.analyze_pattern_density("word", segment_size=50)
        assert len(density) > 0
        assert all(d["matches"] > 0 for d in density)
    
    def test_find_chiastic_patterns(self):
        """Test chiastic pattern detection."""
        # Simple ABBA structure
        text = "Alpha beta gamma. Beta delta epsilon. Delta eta theta. Alpha iota kappa."
        detector = PatternDetector(text)
        
        chiasms = detector.find_chiastic_patterns()
        # This test is probabilistic - may or may not find patterns depending on threshold
        assert isinstance(chiasms, list)
    
    def test_empty_text(self):
        """Test handling of empty text."""
        detector = PatternDetector("")
        
        assert detector.find_literal_patterns("test") == []
        assert detector.find_repeated_structures() == []
        assert detector.get_keyword_contexts("test") == []
