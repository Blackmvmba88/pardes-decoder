"""
Pattern Detector Module - Remez and Derash Layers (Symbolic and Relational)

Provides pattern detection and analysis at multiple semantic levels.
This represents the "R" (Remez) and "D" (Derash) levels - symbolic patterns
and relational/contextual analysis.
"""

import re
from typing import List, Dict, Set, Tuple, Optional, Callable
from collections import defaultdict
from pardes.text_parser import TextParser


class PatternDetector:
    """
    Multi-level pattern detection in text.
    
    Detects:
    - Literal patterns (exact matches, regular expressions)
    - Symbolic patterns (repeated structures, parallel constructions)
    - Relational patterns (co-occurrence, proximity, context)
    """
    
    def __init__(self, text: str = ""):
        """
        Initialize the PatternDetector.
        
        Args:
            text: The text to analyze
        """
        self.text = text
        self.parser = TextParser(text)
    
    def load_text(self, text: str) -> None:
        """
        Load new text for analysis.
        
        Args:
            text: The text to analyze
        """
        self.text = text
        self.parser.load_text(text)
    
    def find_literal_patterns(self, pattern: str, case_sensitive: bool = True) -> List[Dict]:
        """
        Find all occurrences of a literal pattern in the text.
        
        Args:
            pattern: The pattern to search for (can be regex)
            case_sensitive: Whether the search is case-sensitive
            
        Returns:
            List of matches with position and context information
        """
        flags = 0 if case_sensitive else re.IGNORECASE
        matches = []
        
        for match in re.finditer(pattern, self.text, flags=flags):
            # Get context around the match
            start = max(0, match.start() - 50)
            end = min(len(self.text), match.end() + 50)
            context = self.text[start:end]
            
            matches.append({
                'match': match.group(),
                'start': match.start(),
                'end': match.end(),
                'context': context
            })
        
        return matches
    
    def find_repeated_structures(self, min_length: int = 3, 
                                 min_occurrences: int = 2) -> List[Dict]:
        """
        Find repeated structural patterns (sequences of words that repeat).
        
        Args:
            min_length: Minimum length of pattern in characters
            min_occurrences: Minimum number of times pattern must occur
            
        Returns:
            List of repeated patterns with occurrence information
        """
        # Use phrase finding from TextParser
        phrases = self.parser.find_phrases(
            min_words=2, 
            max_words=6, 
            min_frequency=min_occurrences
        )
        
        results = []
        for phrase, count in phrases:
            if len(phrase) >= min_length:
                results.append({
                    'pattern': phrase,
                    'occurrences': count,
                    'type': 'repeated_phrase'
                })
        
        return results
    
    def find_parallel_structures(self, separator: Optional[str] = None) -> List[Dict]:
        """
        Find parallel grammatical structures (sentences/clauses with similar patterns).
        
        Args:
            separator: Optional separator to split text (default: sentence boundaries)
            
        Returns:
            List of parallel structures found
        """
        # Split into segments (sentences by default)
        if separator:
            segments = self.text.split(separator)
        else:
            segments = self.parser.segment_sentences()
        
        # Simple parallel structure detection: similar word patterns
        parallels = []
        
        for i, seg1 in enumerate(segments):
            self.parser.load_text(seg1)
            words1 = self.parser.tokenize_words(lowercase=True)
            
            for j, seg2 in enumerate(segments[i+1:], start=i+1):
                self.parser.load_text(seg2)
                words2 = self.parser.tokenize_words(lowercase=True)
                
                # Check for structural similarity (same length, similar word types)
                if abs(len(words1) - len(words2)) <= 2:
                    common_words = set(words1) & set(words2)
                    if len(common_words) >= min(len(words1), len(words2)) * 0.3:
                        parallels.append({
                            'segment1': seg1.strip(),
                            'segment2': seg2.strip(),
                            'similarity': len(common_words) / max(len(words1), len(words2)),
                            'type': 'parallel_structure'
                        })
        
        # Restore original text
        self.parser.load_text(self.text)
        return parallels
    
    def find_co_occurrences(self, word1: str, word2: str, 
                           window_size: int = 50, 
                           case_sensitive: bool = False) -> List[Dict]:
        """
        Find co-occurrences of two words within a specified window.
        
        Args:
            word1: First word to search for
            word2: Second word to search for
            window_size: Maximum distance (in characters) between words
            case_sensitive: Whether search is case-sensitive
            
        Returns:
            List of co-occurrence instances with context
        """
        text = self.text if case_sensitive else self.text.lower()
        w1 = word1 if case_sensitive else word1.lower()
        w2 = word2 if case_sensitive else word2.lower()
        
        co_occurrences = []
        
        # Find all positions of word1
        pattern1 = r'\b' + re.escape(w1) + r'\b'
        for match1 in re.finditer(pattern1, text):
            # Look for word2 in the window
            window_start = max(0, match1.start() - window_size)
            window_end = min(len(text), match1.end() + window_size)
            window_text = text[window_start:window_end]
            
            pattern2 = r'\b' + re.escape(w2) + r'\b'
            if re.search(pattern2, window_text):
                co_occurrences.append({
                    'word1': word1,
                    'word2': word2,
                    'position1': match1.start(),
                    'context': self.text[window_start:window_end],
                    'type': 'co_occurrence'
                })
        
        return co_occurrences
    
    def find_chiastic_patterns(self) -> List[Dict]:
        """
        Find chiastic patterns (ABBA structures) in text.
        A chiasm is a literary structure where concepts are presented in one order
        and then repeated in reverse order.
        
        Returns:
            List of potential chiastic structures
        """
        sentences = self.parser.segment_sentences()
        chiasms = []
        
        # Look for ABBA patterns in sequences of sentences
        for i in range(len(sentences) - 3):
            seq = sentences[i:i+4]
            
            # Extract key words from each sentence
            self.parser.load_text(seq[0])
            words_a = set(self.parser.tokenize_words(lowercase=True))
            
            self.parser.load_text(seq[1])
            words_b = set(self.parser.tokenize_words(lowercase=True))
            
            self.parser.load_text(seq[2])
            words_b2 = set(self.parser.tokenize_words(lowercase=True))
            
            self.parser.load_text(seq[3])
            words_a2 = set(self.parser.tokenize_words(lowercase=True))
            
            # Check if first and last are similar, and middle two are similar
            ab_similarity = len(words_a & words_a2) / max(len(words_a), len(words_a2), 1)
            ba_similarity = len(words_b & words_b2) / max(len(words_b), len(words_b2), 1)
            
            if ab_similarity > 0.3 and ba_similarity > 0.3:
                chiasms.append({
                    'pattern': 'ABBA',
                    'segments': seq,
                    'ab_similarity': ab_similarity,
                    'ba_similarity': ba_similarity,
                    'type': 'chiastic_structure'
                })
        
        # Restore original text
        self.parser.load_text(self.text)
        return chiasms
    
    def get_keyword_contexts(self, keyword: str, context_size: int = 100,
                            case_sensitive: bool = False) -> List[str]:
        """
        Get all contexts where a keyword appears.
        
        Args:
            keyword: The keyword to search for
            context_size: Number of characters to include on each side
            case_sensitive: Whether search is case-sensitive
            
        Returns:
            List of context strings containing the keyword
        """
        pattern = keyword if case_sensitive else keyword.lower()
        text = self.text if case_sensitive else self.text.lower()
        
        contexts = []
        regex = r'\b' + re.escape(pattern) + r'\b'
        
        for match in re.finditer(regex, text):
            start = max(0, match.start() - context_size)
            end = min(len(text), match.end() + context_size)
            contexts.append(self.text[start:end])
        
        return contexts
    
    def analyze_pattern_density(self, pattern: str, segment_size: int = 500) -> List[Dict]:
        """
        Analyze the density of a pattern across different segments of text.
        
        Args:
            pattern: Pattern to analyze
            segment_size: Size of each segment in characters
            
        Returns:
            List of segments with their pattern density
        """
        results = []
        
        for i in range(0, len(self.text), segment_size):
            segment = self.text[i:i+segment_size]
            matches = len(re.findall(pattern, segment, re.IGNORECASE))
            
            if segment.strip():
                results.append({
                    'start': i,
                    'end': min(i + segment_size, len(self.text)),
                    'pattern': pattern,
                    'matches': matches,
                    'density': matches / len(segment) if segment else 0
                })
        
        return results
