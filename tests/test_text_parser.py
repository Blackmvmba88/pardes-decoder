"""Tests for the text_parser module."""

import pytest
from pardes.text_parser import TextParser


class TestTextParser:
    """Test suite for TextParser class."""
    
    def test_initialization(self):
        """Test parser initialization."""
        parser = TextParser()
        assert parser.text == ""
        
        parser = TextParser("Hello world")
        assert parser.text == "Hello world"
    
    def test_load_text(self):
        """Test loading new text."""
        parser = TextParser("Initial text")
        parser.load_text("New text")
        assert parser.text == "New text"
    
    def test_segment_sentences(self):
        """Test sentence segmentation."""
        text = "Hello world. How are you? I am fine!"
        parser = TextParser(text)
        sentences = parser.segment_sentences()
        
        assert len(sentences) == 3
        assert sentences[0] == "Hello world."
        assert sentences[1] == "How are you?"
        assert sentences[2] == "I am fine!"
    
    def test_tokenize_words(self):
        """Test word tokenization."""
        text = "Hello, world! How are you?"
        parser = TextParser(text)
        words = parser.tokenize_words()
        
        assert "Hello" in words
        assert "world" in words
        assert "How" in words
        assert "," not in words
        assert "!" not in words
    
    def test_tokenize_words_lowercase(self):
        """Test word tokenization with lowercase."""
        text = "Hello World"
        parser = TextParser(text)
        words = parser.tokenize_words(lowercase=True)
        
        assert "hello" in words
        assert "world" in words
        assert "Hello" not in words
    
    def test_word_frequency(self):
        """Test word frequency calculation."""
        text = "the cat and the dog and the bird"
        parser = TextParser(text)
        freq = parser.get_word_frequency()
        
        assert freq["the"] == 3
        assert freq["and"] == 2
        assert freq["cat"] == 1
        assert freq["dog"] == 1
        assert freq["bird"] == 1
    
    def test_character_frequency(self):
        """Test character frequency calculation."""
        text = "aabbcc"
        parser = TextParser(text)
        freq = parser.get_character_frequency()
        
        assert freq["a"] == 2
        assert freq["b"] == 2
        assert freq["c"] == 2
    
    def test_statistics(self):
        """Test text statistics."""
        text = "Hello world. This is a test."
        parser = TextParser(text)
        stats = parser.get_statistics()
        
        assert stats["character_count"] == len(text)
        assert stats["word_count"] == 6
        assert stats["sentence_count"] == 2
        assert stats["unique_words"] > 0
        assert stats["avg_word_length"] > 0
        assert stats["avg_sentence_length"] > 0
    
    def test_find_phrases(self):
        """Test repeated phrase detection."""
        text = "the quick brown fox jumps over the quick brown dog"
        parser = TextParser(text)
        phrases = parser.find_phrases(min_words=2, min_frequency=2)
        
        # Should find "the quick brown"
        phrase_texts = [p[0] for p in phrases]
        assert "the quick brown" in phrase_texts
    
    def test_normalize_text(self):
        """Test text normalization."""
        text = "Hello, World! How are you?"
        parser = TextParser(text)
        normalized = parser.normalize_text()
        
        assert "," not in normalized
        assert "!" not in normalized
        assert "?" not in normalized
        assert normalized.islower()
    
    def test_empty_text(self):
        """Test handling of empty text."""
        parser = TextParser("")
        
        assert parser.segment_sentences() == []
        assert parser.tokenize_words() == []
        assert parser.get_word_frequency() == {}
        stats = parser.get_statistics()
        assert stats["word_count"] == 0
