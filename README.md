# PyHound 

**Hunt down retrieval problems. Fix them fast.**

PyHound is a diagnostic tool for RAG/LLM retrieval systems that tells you exactly why your retrieval is failing—not just that it is.

## Features

-  **Component Diagnosis** — Isolate failures to embedding, vector search, keyword search, or reranker
-  **Plain English Explanations** — Understand what's wrong without metrics jargon
-  **Model Comparison** — Compare embedding and reranker models side-by-side with quality/cost trade-offs
-  **Improvement Tracking** — See exactly what got better after applying a fix (BM25 +5%, Vector +12%, etc.)
-  **Drift Detection** — Monitor embedding quality degradation in production
- 🗄️ **Database-Agnostic** — Works with Qdrant, Chroma, Pinecone, Milvus, Weaviate, or any vector DB

## Quick Start

### Installation

```bash
# Using pip
pip install pyhound

# Using uv
uv pip install pyhound

# Or download binary
curl -sSL https://github.com/Mullassery/pyhound/releases/latest/download/pyhound -o pyhound
chmod +x pyhound
```

### Basic Usage

```python
from pyhound import Hound

# Point to your vector database
hound = Hound(db="qdrant", endpoint="localhost:6333")

# Diagnose a failing query
diagnosis = hound.diagnose(
    query="your search query",
    top_k=5,
    expected_docs=[...]  # optional ground truth
)

# Get plain English report
print(diagnosis.hunt())
```

### Example Output

```
═══════════════════════════════════════════════════════════════
                    PyHound Diagnosis Report
═══════════════════════════════════════════════════════════════

Query: "quantum computing"
Status:  RETRIEVAL DEGRADED (F1: 0.52)

 COMPONENT ANALYSIS
─────────────────────────────────────────────────────────────

EMBEDDING MODEL:  WEAK
  • Isotropy 45% (should be >70%)
  • Distinctiveness 21% (should be >60%)
  → Problem: Model too generic for your domain

VECTOR SEARCH:  MODERATE
  • Precision 62% (should be >85%)
  → Impact: 38% wrong results

KEYWORD SEARCH:  GOOD
  • Precision 85%, Recall 78%
  → Status: Working well

RERANKER:  GOOD
  • Calibration 91%
  → Impact: Doing its job, can't fix upstream issues


ROOT CAUSE
─────────────────────────────────────────────────────────────
Your embedding model (text-embedding-3-small) doesn't understand
domain-specific concepts. Vector search is failing because of this.


HOW TO FIX IT (Ranked by Impact)
─────────────────────────────────────────────────────────────
1.  HIGHEST ROI: Upgrade embedding model
   Try: text-embedding-3-large OR domain-specific model
   Quality gain: +8-12 F1 points
   Cost: +$8/month
   Time: 2 hours

2. ⚙️ Quick win: Adjust hybrid weights
   Current: BM25 (50%) + Vector (50%)
   Try: BM25 (40%) + Vector (60%)
   Quality gain: +2-3 F1 points
   Time: 10 minutes
```

## Core Features

### 1. Diagnosis
Isolate which component failed and understand why.

```python
diagnosis = hound.diagnose(query="...", top_k=5)
print(diagnosis.hunt())           # Plain English report
print(diagnosis.metrics())        # Raw metrics
print(diagnosis.recommendations()) # Ranked fixes
```

### 2. Model Comparison
Compare embedding and reranker models with quality/cost analysis.

```python
comparison = hound.compare_models(
    model_type="embedding",
    candidates=["3-small", "3-large", "cohere-v3"]
)
print(comparison.report())  # Quality, cost, latency, ROI

# A/B test before committing
ab_test = comparison.ab_test(
    model_a="3-small",
    model_b="3-large",
    duration_days=7
)
```

### 3. Improvement Tracking
Measure what actually improved after applying a fix.

```python
improvement = hound.compare_metrics(
    before="2026-06-15",
    after="2026-06-20"
)
print(improvement.breakdown())
# Shows: Vector +25.8%, BM25 +1.1%, Overall +36.5%
```

### 4. Quality Scoring
Monitor embedding quality in real-time.

```python
scorer = hound.quality_scorer()

# Score individual embedding
quality = scorer.score(embedding_vector)
# Returns: isotropy, coverage, distinctiveness, status

# Monitor corpus health
health = scorer.corpus_health()
# Returns: trend, drift_percentage, anomalies
```

### 5. Drift Detection
Get alerts when embedding quality degrades.

```python
drift = hound.detect_drift(
    baseline_date="2026-01-01",
    current_date="2026-06-20"
)

if drift.significant:
    print(f"Quality degraded {drift.amount}%")
    print(f"Recommended fix: {drift.recommendation}")
```

## Supported Vector Databases

-  **Qdrant** — Full support
-  **Chroma** — Full support
-  **Pinecone** — Full support
-  **Milvus** — Full support
-  **Weaviate** — Full support
-  **PostgreSQL (pgvector)** — Full support
-  **Custom** — Query any database

Add more databases by implementing the `VectorDB` protocol.

## Architecture

```
Rust Core (pyhound_core)
├─ Embedding quality metrics
├─ Pipeline analysis
├─ Drift detection
└─ Improvement tracking
    ↓ (PyO3 bindings)
Python Wrapper
└─ Hound class (main API)
```

**Why Rust?**
- Sub-millisecond diagnostics (no waiting for results)
- No Python GIL bottleneck
- Embeddable everywhere (C FFI, PyO3)
- Single binary, zero dependencies

## PyHound vs Observability Tools

PyHound is **not** a replacement for observability platforms like Phoenix, Arize, or Helicone.

| Tool | Purpose | Answers |
|------|---------|---------|
| **Phoenix/Arize** | Monitor what's happening | "Is something broken?" |
| **PyHound** | Diagnose problems | "What's broken and why?" |
| **PyHound** | Guide solutions | "How do I fix it?" |
| **PyHound** | Measure results | "Did my fix work?" |

**Ideal setup:** Use both—observability alerts you, PyHound diagnoses and fixes.

## Documentation

- [Installation Guide](docs/installation.md)
- [User Guide](docs/guide.md)
- [API Reference](docs/api.md)
- [Examples](examples/)
- [Contributing](CONTRIBUTING.md)

## Examples

See the [examples/](examples/) directory for:
- Basic diagnosis workflow
- Model comparison and selection
- Integration with LlamaIndex
- Integration with Haystack
- Custom database adapters

## Performance

- **Diagnosis latency:** <100ms per query
- **Quality scoring:** <1ms per embedding
- **Corpus analysis:** <500ms for 100k documents

## Requirements

- Python 3.8+
- Rust 1.70+ (for building from source)
- Vector DB client (Qdrant, Chroma, etc.)

## License

MIT License — See [LICENSE](LICENSE) for details.

PyHound is free for commercial use.

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Roadmap

- **v0.1** — Embedding Inspector + basic diagnostics
- **v0.2** — Hybrid retrieval engine (BM25 + vector + reranker)
- **v0.3** — Embedding versioning with zero-downtime migrations
- **v1.0** — Advanced optimization tools, full observability integration

## Support

- 💬 [GitHub Discussions](https://github.com/Mullassery/pyhound/discussions)
- 🐛 [Issue Tracker](https://github.com/Mullassery/pyhound/issues)
- 📧 Email: mullassery@gmail.com

## Authors

- **Georgi Mammen Mullassery** — Original creator

## Acknowledgments

Built with:
- Rust ecosystem (fast, safe, embeddable)
- PyO3 (Python bindings)
- Open source community

---

**Hunt down retrieval problems. Fix them fast.** 
