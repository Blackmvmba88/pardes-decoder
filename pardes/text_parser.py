"""
Text Parser Module - Peshat Layer (Literal/Surface Level)

Provides text parsing, segmentation, and basic analysis tools.
This represents the "P" (Peshat) level - literal, surface-level text processing.
"""

import re
from typing import List, Dict, Tuple
from collections import Counter


class TextParser:
    """
    Parser for text segmentation and basic linguistic analysis.
    
    Provides methods for:
    - Sentence segmentation
    - Word tokenization
    - Character and word frequency analysis
    - Basic text statistics
    """
    
    def __init__(self, text: str = ""):
        """
        Initialize the TextParser with optional text.
        
        Args:
            text: The text to parse
        """
        self.text = text
        self._sentences = None
        self._words = None
        self._tokens = None
    
    def load_text(self, text: str) -> None:
        """
        Load new text into the parser.
        
        Args:
            text: The text to parse
        """
        self.text = text
        self._sentences = None
        self._words = None
        self._tokens = None
    
    def segment_sentences(self) -> List[str]:
        """
        Segment text into sentences using basic punctuation rules.
        
        Returns:
            List of sentences
        """
        if self._sentences is None:
            # Simple sentence segmentation using punctuation
            # Handle common abbreviations
            text = self.text
            # Split on sentence-ending punctuation followed by space and capital letter
            pattern = r'(?<=[.!?])\s+(?=[A-Z])'
            sentences = re.split(pattern, text)
            self._sentences = [s.strip() for s in sentences if s.strip()]
        return self._sentences
    
    def tokenize_words(self, lowercase: bool = False) -> List[str]:
        """
        Tokenize text into words, removing punctuation.
        
        Args:
            lowercase: Whether to convert words to lowercase
            
        Returns:
            List of word tokens
        """
        # Extract words (sequences of letters, numbers, and hyphens)
        pattern = r'\b[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*\b'
        tokens = re.findall(pattern, self.text)
        
        if lowercase:
            tokens = [t.lower() for t in tokens]
        
        return tokens
    
    def get_word_frequency(self, lowercase: bool = True, min_length: int = 1) -> Dict[str, int]:
        """
        Calculate word frequency distribution.
        
        Args:
            lowercase: Whether to normalize to lowercase
            min_length: Minimum word length to include
            
        Returns:
            Dictionary mapping words to their frequencies
        """
        words = self.tokenize_words(lowercase=lowercase)
        words = [w for w in words if len(w) >= min_length]
        return dict(Counter(words))
    
    def get_character_frequency(self, include_spaces: bool = False) -> Dict[str, int]:
        """
        Calculate character frequency distribution.
        
        Args:
            include_spaces: Whether to include spaces in the count
            
        Returns:
            Dictionary mapping characters to their frequencies
        """
        text = self.text if include_spaces else self.text.replace(' ', '')
        return dict(Counter(text))
    
    def get_statistics(self) -> Dict[str, int]:
        """
        Get basic text statistics.
        
        Returns:
            Dictionary with character count, word count, sentence count, etc.
        """
        sentences = self.segment_sentences()
        words = self.tokenize_words()
        
        return {
            'character_count': len(self.text),
            'word_count': len(words),
            'sentence_count': len(sentences),
            'unique_words': len(set(w.lower() for w in words)),
            'avg_word_length': sum(len(w) for w in words) / len(words) if words else 0,
            'avg_sentence_length': len(words) / len(sentences) if sentences else 0,
        }
    
    def find_phrases(self, min_words: int = 2, max_words: int = 5, 
                     min_frequency: int = 2) -> List[Tuple[str, int]]:
        """
        Find repeated phrases in the text.
        
        Args:
            min_words: Minimum number of words in a phrase
            max_words: Maximum number of words in a phrase
            min_frequency: Minimum number of times a phrase must appear
            
        Returns:
            List of (phrase, frequency) tuples, sorted by frequency
        """
        words = self.tokenize_words(lowercase=True)
        phrases = []
        
        for n in range(min_words, max_words + 1):
            for i in range(len(words) - n + 1):
                phrase = ' '.join(words[i:i+n])
                phrases.append(phrase)
        
        phrase_counts = Counter(phrases)
        repeated = [(p, c) for p, c in phrase_counts.items() if c >= min_frequency]
        repeated.sort(key=lambda x: x[1], reverse=True)
        
        return repeated
    
    def normalize_text(self, remove_punctuation: bool = True, 
                       lowercase: bool = True) -> str:
        """
        Normalize text by optionally removing punctuation and converting to lowercase.
        
        Args:
            remove_punctuation: Whether to remove punctuation
            lowercase: Whether to convert to lowercase
            
        Returns:
            Normalized text string
        """
        text = self.text
        
        if remove_punctuation:
            # Keep letters, numbers, and spaces
            text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
            # Normalize whitespace
            text = re.sub(r'\s+', ' ', text).strip()
        
        if lowercase:
            text = text.lower()
        
        return text
