# PyHound Architecture

## Overview

PyHound is a diagnostic tool for RAG/LLM retrieval systems, built with:
- **Rust core** — High-performance diagnostics
- **Python wrapper** — Easy integration with Python ML workflows

```
┌─────────────────────────────────────────────────────────────┐
│ User Application (Python)                                   │
│ from pyhound import Hound                                   │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│ PyHound Python API (pyhound/)                               │
│ ├─ Hound (main interface)                                  │
│ ├─ Diagnosis (analysis results)                            │
│ ├─ ModelComparison (model selection)                       │
│ └─ QualityScorer (embedding monitoring)                    │
└─────────────────────┬───────────────────────────────────────┘
                      │ (PyO3 bindings)
┌─────────────────────▼───────────────────────────────────────┐
│ PyHound Rust Core (src/lib.rs)                              │
│ ├─ Isotropy calculation                                    │
│ ├─ Coverage analysis                                       │
│ ├─ Distinctiveness metrics                                 │
│ ├─ Drift detection                                         │
│ ├─ Component analysis                                      │
│ └─ Improvement tracking                                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│ Database Adapters                                           │
│ ├─ Qdrant adapter                                          │
│ ├─ Chroma adapter                                          │
│ ├─ Pinecone adapter                                        │
│ ├─ Milvus adapter                                          │
│ └─ Weaviate adapter                                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│ Vector Databases                                            │
│ ├─ Qdrant                                                  │
│ ├─ Chroma                                                  │
│ ├─ Pinecone                                                │
│ ├─ Milvus                                                  │
│ └─ Weaviate                                                │
└─────────────────────────────────────────────────────────────┘
```

## Core Concepts

### Components

PyHound analyzes retrieval at four stages:

1. **Embedding Quality** — How well embeddings capture semantics
   - Isotropy: Vector space utilization
   - Coverage: Diversity of embeddings
   - Distinctiveness: Semantic separation

2. **Vector Search** — Similarity matching quality
   - Precision: Correctness of results
   - Recall: Completeness of results
   - Ranking quality: Relevance ordering

3. **Keyword Search (BM25)** — Full-text matching
   - Precision and recall
   - Match quality

4. **Reranker** — Final result ordering
   - Calibration: Are scores correct?
   - NDCG: Ranking quality

### Diagnosis Flow

```
User Query
    │
    ├─→ Retrieve results (vector DB)
    │
    ├─→ Compute metrics for each component:
    │   ├─ Embedding quality (Rust core)
    │   ├─ Vector search metrics
    │   ├─ BM25 metrics
    │   └─ Reranker metrics
    │
    ├─→ Identify root cause
    │
    ├─→ Generate recommendations
    │
    └─→ Return Diagnosis object
```

## Key Modules

### `pyhound/hound.py`
Main interface. Coordinates diagnosis, comparison, and monitoring.

### `pyhound/diagnosis.py`
Analyzes retrieval failures and generates reports.

### `pyhound/comparison.py`
Compares models (embedding, reranker) for selection.

### `pyhound/scorer.py`
Monitors embedding quality in production.

### `src/lib.rs`
Rust core implementing:
- Embedding metrics (isotropy, coverage, distinctiveness)
- Drift detection
- Performance-critical calculations

## Data Flow

### Diagnosis Request

```python
hound = Hound(db="qdrant")
diagnosis = hound.diagnose(query="...", top_k=5)
```

1. Query is sent to vector database
2. Top-K results retrieved
3. Rust core computes metrics
4. Python layer analyzes results
5. Diagnosis object generated with recommendations

### Model Comparison

```python
comparison = hound.compare_models(
    model_type="embedding",
    candidates=["3-small", "3-large"]
)
```

1. Sample queries selected
2. Each model tested on samples
3. Metrics computed (quality, cost, latency)
4. Recommendations generated

## Performance Considerations

- **Rust core** — Sub-millisecond metric calculations
- **Database queries** — Depends on database (typically 1-100ms)
- **Python overhead** — Minimal via PyO3
- **Caching** — Results cached when possible

Target: <100ms end-to-end diagnosis per query

## Extensibility

### Adding Database Adapters

Implement the `VectorDB` protocol:

```python
class CustomDBAdapter(VectorDB):
    def connect(self, endpoint: str) -> None: ...
    def search(self, query: np.ndarray, top_k: int) -> List[Result]: ...
    def get_embeddings(self, doc_ids: List[str]) -> List[np.ndarray]: ...
```

### Adding Metrics

Rust functions are exposed via PyO3:

```rust
#[pyfunction]
fn compute_custom_metric(embeddings: Vec<Vec<f32>>) -> PyResult<f32> {
    // Implementation
}
```

## Testing Strategy

- **Unit tests** — Rust metrics calculation
- **Integration tests** — Full diagnosis workflow
- **Database tests** — Each adapter
- **Benchmark tests** — Performance regressions

See `tests/` for examples.
