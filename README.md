# PaRDeS Decoder

**Computational Analysis of Layered Textual Meaning**

A Python framework for rigorous, multi-level text analysis inspired by the PaRDeS interpretive framework, implemented using formal computational methods without mystical or theological assumptions.

## Overview

PaRDeS Decoder provides tools for analyzing text at four computational levels, inspired by the traditional PaRDeS framework:

- **P (Peshat/Literal)**: Surface-level text parsing, segmentation, and statistical analysis
- **R (Remez/Symbolic)**: Pattern detection, repeated structures, and symbolic analysis
- **D (Derash/Relational)**: Contextual analysis, co-occurrence, and relationship detection
- **S (Sod/Integrative)**: Graph-based semantic networks and integrative analysis

## Features

### Text Parsing Module (`TextParser`)
- Sentence segmentation
- Word tokenization
- Character and word frequency analysis
- Phrase detection
- Text statistics and normalization

### Pattern Detection Module (`PatternDetector`)
- Literal pattern matching (regex support)
- Repeated structure detection
- Parallel construction analysis
- Co-occurrence analysis
- Chiastic pattern detection
- Keyword context extraction
- Pattern density analysis

### Semantic Graph Module (`SemanticGraph`)
- Co-occurrence network construction
- Sentence similarity graphs
- Custom concept relationship graphs
- Centrality analysis (degree, betweenness, closeness, eigenvector)
- Community detection
- Path finding and neighborhood analysis
- Graph statistics and export capabilities

## Installation

```bash
# Clone the repository
git clone https://github.com/Blackmvmba88/pardes-decoder.git
cd pardes-decoder

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Quick Start

```python
from pardes import TextParser, PatternDetector, SemanticGraph

# Parse text at the literal level
text = "Your text here. Multiple sentences work well."
parser = TextParser(text)
stats = parser.get_statistics()
sentences = parser.segment_sentences()
word_freq = parser.get_word_frequency()

# Detect patterns
detector = PatternDetector(text)
patterns = detector.find_repeated_structures()
co_occurs = detector.find_co_occurrences("word1", "word2")

# Build semantic networks
graph = SemanticGraph()
graph.build_cooccurrence_graph(text, window_size=5)
central_concepts = graph.get_central_concepts(top_n=10)
communities = graph.find_communities()
```

## Examples

The `examples/` directory contains comprehensive demonstrations:

- `01_text_parsing.py` - Text parsing and statistics (Peshat layer)
- `02_pattern_detection.py` - Pattern analysis (Remez/Derash layers)
- `03_semantic_graphs.py` - Semantic networks (Sod layer)
- `04_comprehensive_analysis.py` - Complete multi-layer analysis

Run examples:
```bash
python examples/01_text_parsing.py
python examples/04_comprehensive_analysis.py
```

## Testing

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run tests with coverage
pytest --cov=pardes --cov-report=html
```

## Methodology

This framework interprets the PaRDeS levels computationally:

1. **Literal Analysis (Peshat)**: Uses NLP techniques for tokenization, segmentation, and statistical analysis
2. **Symbolic Analysis (Remez)**: Employs pattern matching algorithms and structural detection
3. **Relational Analysis (Derash)**: Applies co-occurrence analysis and contextual relationship detection
4. **Integrative Analysis (Sod)**: Utilizes graph theory and network analysis for holistic understanding

All methods are grounded in:
- Computational linguistics
- Statistical text analysis
- Graph theory and network science
- Formal pattern recognition

No mystical, theological, or supernatural assumptions are made. The framework provides objective, reproducible analysis suitable for academic research and text analytics applications.

## Use Cases

- Literary analysis and text mining
- Content analysis and information extraction
- Document clustering and classification
- Semantic network visualization
- Educational text analysis tools
- Digital humanities research

## Requirements

- Python >= 3.8
- NetworkX >= 2.6 (graph analysis)
- NumPy >= 1.20 (numerical operations)
- Matplotlib >= 3.3 (visualization support)

## Contributing

Contributions are welcome! This project emphasizes:
- Scientific rigor and reproducibility
- Clear documentation
- Comprehensive testing
- Modular, maintainable code

## License

MIT License - see LICENSE file for details.

## Citation

If you use this framework in academic work, please cite:

```
PaRDeS Decoder: Computational Analysis of Layered Textual Meaning
https://github.com/Blackmvmba88/pardes-decoder
```

## Acknowledgments

This framework is inspired by traditional textual interpretation methods, reimagined through the lens of modern computational linguistics and data science.
