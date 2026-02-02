"""
PaRDeS Decoder - Computational Analysis of Layered Textual Meaning

This package provides tools for computational analysis of texts using methods
inspired by the PaRDeS framework, focusing on:
- Text parsing and segmentation
- Multi-level pattern detection
- Graph-based semantic structures
- Reproducible scientific analysis

The name PaRDeS traditionally refers to four levels of textual interpretation,
which we interpret computationally as:
- P (Peshat/Literal): Surface-level text parsing and pattern matching
- R (Remez/Symbolic): Symbolic and metaphorical pattern detection
- D (Derash/Relational): Relationship and contextual analysis
- S (Sod/Integrative): Integrated semantic network analysis

This implementation focuses on formal, computational methods without mystical
or theological assumptions.
"""

__version__ = "0.1.0"
__author__ = "BlackMamba"

from pardes.text_parser import TextParser
from pardes.pattern_detector import PatternDetector
from pardes.semantic_graph import SemanticGraph

__all__ = [
    "TextParser",
    "PatternDetector",
    "SemanticGraph",
]
