# PyHound — Retrieval Diagnostics for RAG/LLM Teams

**Name:** PyHound  
**Tagline:** *"Hunt down retrieval problems. Fix them fast."*  
**Stack:** Rust core (performance) + Python wrapper (DX)  
**License:** MIT (open source, commercial-friendly)  

---

## What Is PyHound?

A diagnostic tool that hunts down which part of your retrieval pipeline is broken.

**The Problem:** Your RAG quality dropped. F1-score fell from 0.87 to 0.52. Is it the embedding model? Vector search? Keyword matching? The reranker? You don't know.

**PyHound's Answer:** Isolate the exact component that failed. Explain it in plain English. Show you how to fix it. Measure improvement by component.

---

## Core Value Proposition

### **"Know Exactly What's Broken in Your Retrieval"**

When retrieval fails, PyHound:
1. ✅ **Diagnoses the component** — embedding, vector search, BM25, or reranker
2. ✅ **Explains why** — Plain English, not metrics
3. ✅ **Recommends fixes** — Ranked by impact and cost
4. ✅ **Compares models** — Embedding + reranker side-by-side
5. ✅ **Tracks improvement** — What actually got better and by how much

---

## Why PyHound (Not Just Another Tool)

### Validation: This is a Real Problem

Evidence from market research:
- ✅ [Academic research](https://arxiv.org/abs/2504.13587) — "Developers struggle to identify which RAG component failed"
- ✅ [RAG debugging guides](https://www.getmaxim.ai/articles/rag-debugging-identifying-issues-in-retrieval-augmented-generation/) — "Retrieval is the most frequent failure point"
- ✅ [Expert consensus](https://medium.com/@Modexa/your-rag-isnt-ready-until-you-can-debug-retrieval-fffd1ad6522c) — "Your RAG isn't ready until you can debug retrieval"
- ✅ Teams currently debug blind — manual parameter tweaking, no diagnostics
- ✅ No existing tool isolates component failures (DeepEval measures overall, not components)

### What Makes PyHound Different

| Aspect | DeepEval | Evidently | Galileo AI | **PyHound** |
|--------|----------|-----------|-----------|-----------|
| **Component diagnosis** | ❌ | ❌ | 🟡 (closed) | ✅ |
| **Plain English** | ❌ | ❌ | ❌ | ✅ |
| **Works with any DB** | ❌ | ❌ | ❌ | ✅ |
| **Model comparison** | ❌ | ❌ | ❌ | ✅ |
| **Open source (MIT)** | ✅ | ✅ | ❌ | ✅ |
| **Production monitoring** | ❌ | ✅ | ✅ | ✅ |

**Key differentiator:** PyHound is the only tool that isolates which retrieval component failed AND explains it in plain English AND compares models.

---

## PyHound in Action

### Example 1: Diagnosis

```python
from pyhound import Hound

# Point to your vector DB (Qdrant, Chroma, Pinecone, etc.)
hound = Hound(db="qdrant", endpoint="localhost:6333")

# Diagnose a failing query
diagnosis = hound.diagnose(
    query="quantum computing",
    expected_docs=[doc_ids...],  # optional ground truth
    top_k=5
)

print(diagnosis.hunt())
# Output:
"""
═══════════════════════════════════════════════════════════════
                    PyHound Diagnosis Report
═══════════════════════════════════════════════════════════════

Query: "quantum computing"
Status: ⚠️ RETRIEVAL DEGRADED (F1: 0.52)

HUNTING DOWN THE PROBLEM
─────────────────────────────────────────────────────────────

🔍 Stage 1: EMBEDDING MODEL
   Status: ❌ WEAK (This is your problem!)
   
   Problem: Your embedding model (text-embedding-3-small) doesn't
           understand domain-specific concepts like "quantum coherence"
   
   Metrics:
   • Isotropy: 45% (should be >70%)   ← Vectors clustering
   • Distinctiveness: 21% (should be >60%) ← Concepts look similar
   
   Impact: Vector search can't find relevant docs

🔍 Stage 2: VECTOR SEARCH
   Status: ⚠️ MODERATE (Impacted by #1)
   
   Precision: 62% (should be >85%)
   Impact: 38% of results are wrong

🔍 Stage 3: KEYWORD SEARCH (BM25)
   Status: ✅ GOOD
   
   Precision: 85% | Recall: 78%
   Impact: Working well! Catching results vector search misses

🔍 Stage 4: RERANKER
   Status: ✅ GOOD (But limited by #1)
   
   Calibration: 91%
   Impact: Doing its job, but can't fix poor upstream results


ROOT CAUSE IDENTIFIED
─────────────────────────────────────────────────────────────
🎯 Primary: Embedding model too generic for your domain
🎯 Secondary: Vector search quality degraded as a result


HOW TO FIX IT (Ranked by Impact)
─────────────────────────────────────────────────────────────
1. 💰 HIGHEST ROI: Upgrade embedding model
   Try: text-embedding-3-large OR domain-specific model
   Expected quality gain: +8-12 F1 points
   Cost impact: +$8/month OR +5% API costs
   Time to implement: 2 hours
   
2. ⚙️ Quick win: Adjust hybrid weights
   Current: BM25 (50%) + Vector (50%)
   Try: BM25 (40%) + Vector (60%)
   Expected gain: +2-3 F1 points
   Time: 10 minutes

3. 🔧 Optional: Fine-tune embedding on your corpus
   If you have >500 labeled examples
   Expected: +5-8% quality
   Time: 1-2 days


WHAT DIDN'T CHANGE (Good News)
─────────────────────────────────────────────────────────────
✅ BM25 (keyword search) is working fine
✅ This confirms the problem is in embeddings, not keywords
"""

# Get specific metrics if you need them
print(diagnosis.metrics())
```

### Example 2: Model Comparison

```python
# Compare embedding models before upgrading
comparison = hound.compare_models(
    model_type="embedding",
    candidates=[
        "text-embedding-3-small",      # current
        "text-embedding-3-large",      # expensive
        "cohere-v3",                   # alternative
    ]
)

print(comparison.report())
# Output:
"""
EMBEDDING MODEL COMPARISON
═════════════════════════════════════════════════════════════

                      F1    Cost/1M   Speed   ROI
─────────────────────────────────────────────────────────────
🏆 Best Quality
   3-large               0.76  $2.00    2.1ms  ⭐⭐⭐
   (+8.5% quality, +40% cost)

💰 Best Value
   cohere-v3            0.74  $1.50    3.2ms  ⭐⭐
   (+5.7% quality, +30% cost)

📊 Baseline (current)
   3-small              0.70  $0.02    1.8ms  ⭐
   
💡 Budget Option
   sentence-transformers 0.68 $0.00    4.1ms  🆓
   (-2.8% quality, free)

═════════════════════════════════════════════════════════════

Recommendation:
→ Upgrade to text-embedding-3-large for +8.5% quality
→ Or use cohere-v3 for better value (+5.7%, cheaper)
"""
```

### Example 3: Track Improvements

```python
# After applying a fix, measure the impact
improvement = hound.compare_metrics(
    before="2026-06-15",  # before upgrade
    after="2026-06-20"    # after upgrade
)

print(improvement.breakdown())
# Output:
"""
IMPROVEMENT TRACKING
═════════════════════════════════════════════════════════════

Overall F1: 0.52 → 0.71 (↑ 36.5%) ✅


WHAT IMPROVED (by component)
─────────────────────────────────────────────────────────────
1. Vector Precision: 0.62 → 0.78 (↑ 25.8%) 🎯
   → Embedding upgrade to 3-large helped!
   → Isotropy improved 45% → 72%

2. Reranker NDCG:   0.73 → 0.75 (↑ 2.7%)
   → Minor improvement (was already good)

3. BM25 Precision:  0.85 → 0.86 (↑ 1.1%)
   → Unchanged (was working fine)


WHAT DIDN'T CHANGE (Good News)
─────────────────────────────────────────────────────────────
✅ BM25 stable — confirms vector was the bottleneck
✅ Reranker stable — doing its job
✅ No unexpected side effects


COST-BENEFIT ANALYSIS
─────────────────────────────────────────────────────────────
Cost increase: +$8/month
Quality gain: +36.5% F1-score
ROI: ✅ EXCELLENT
Break-even: Immediate (better results = more engagement)
"""
```

---

## Key Features

### 1. Component-Level Diagnostics
Isolates failures to: embedding → vector search → BM25 → reranker

### 2. Plain English Explanations
No "isotropy 0.45" — explains what it means and why it matters

### 3. Multi-Model Comparison
Compare embedding models, rerankers, LLMs side-by-side with quality/cost/speed

### 4. Improvement Tracking
Shows what actually got better after you applied a fix

### 5. Drift Detection
Warns when embedding quality degrades (automatic monitoring)

### 6. Database-Agnostic
Works with Qdrant, Chroma, Pinecone, Milvus, Weaviate (or any vector DB)

---

## Installation

### Option 1: pip (recommended)
```bash
pip install pyhound-core
```

### Option 2: uv
```bash
uv pip install pyhound-core
```

### Option 3: Direct download
```bash
# Get the Rust binary
curl -sSL https://github.com/pyhound-ai/releases/latest/download/pyhound -o pyhound
chmod +x pyhound

# Use standalone
./pyhound diagnose --query "your query" --db qdrant
```

### Quick Start (2 minutes)
```python
from pyhound import Hound

hound = Hound(db="qdrant", endpoint="localhost:6333")
diagnosis = hound.diagnose(query="your query", top_k=5)
print(diagnosis.hunt())  # Plain English report
```

---

## Market Position

### Problem We Solve
- **DeepEval** measures RAG quality (good for testing)
- **Evidently** monitors data drift (good for generic monitoring)
- **Galileo AI** debugs RAG (good but closed, cloud-only)
- **PyHound** diagnoses retrieval component failures (missing piece)

### Why PyHound Fills the Gap
1. ✅ Component-level isolation (which part failed?)
2. ✅ Production diagnostics (not just testing)
3. ✅ Database-agnostic (use with your current setup)
4. ✅ Plain English recommendations
5. ✅ Open source, MIT licence (no vendor lock-in)

---

## Who Should Use PyHound

**✅ Teams building RAG/LLM applications**
- Struggling with retrieval quality issues
- Need to debug without ripping out their stack
- Want to optimize model selection

**✅ Teams using vector databases**
- Qdrant, Chroma, Pinecone, Milvus, Weaviate
- Want production observability
- Don't want cloud-only solutions

**✅ Small-to-medium teams**
- Cost-conscious (open source, free)
- Need fast debugging (plain English reports)
- Want to own their diagnostics (no vendor lock-in)

---

## The Hound Approach

PyHound's philosophy: **Hunt down the problem, don't guess.**

| Traditional Approach | PyHound Approach |
|---|---|
| F1 drops → Guess | F1 drops → Diagnose |
| Try random fixes | Try targeted fixes |
| Waste time/money | Save time/money |
| Surprised by costs | Predict costs |
| Fix one thing, break another | Know exactly what improved |

---

## Next Steps

1. **Try PyHound** — `pip install pyhound-core`
2. **Point it at your DB** — `Hound(db="qdrant", ...)`
3. **Run diagnosis** — `hound.diagnose(query, top_k=5)`
4. **Get plain English report** — `print(diagnosis.hunt())`
5. **Fix with confidence** — You know what's wrong now

---

## Technical Stack

- **Core:** Rust (sub-millisecond diagnostics, no GIL)
- **Python binding:** PyO3 (simple, familiar API)
- **Supported DBs:** Qdrant, Chroma, Pinecone, Milvus, Weaviate, custom
- **License:** MIT (commercial-friendly, no restrictions)

---

## The PyHound Promise

> **"You'll know why your retrieval failed, not just that it did."**

Stop guessing. Start hunting.
