# Automated Research Pipeline v1.0
## Efficient Knowledge Extraction from Free Sources

**Status:** Architecture + Engine Built | Integration Layer Ready  
**Efficiency:** 3-stage progressive pipeline with early exits | Minimal API calls  
**Coverage:** 8 free sources across 7 research domains

---

## The Problem

Manual research is:
- **Time-intensive:** Searching each source individually
- **Redundant:** Finding same papers multiple times
- **Unfocused:** No strategy for source selection
- **Unstructured:** Results scattered across tabs and notes

**Solution:** Automated pipeline that searches intelligently, stops early when saturation reached, and outputs structured findings.

---

## Architecture Overview

```
Query Input → Domain Detection → Source Selection
                    ↓
        ┌─────────────────────┐
        │    STAGE 1: QUICK   │
        │    SIGNAL CHECK     │
        │ (Wikipedia + Scholar)
        └──────────┬──────────┘
                   ↓
        [Gate 1: Is there signal?]
             │                │
             YES              NO → Exit (query not researchable)
             ↓
        ┌─────────────────────┐
        │    STAGE 2: DEEP    │
        │    RESEARCH         │
        │ (PubMed, arXiv,     │
        │  Semantic Scholar)  │
        └──────────┬──────────┘
                   ↓
        [Early Exit if Saturation (15+ high-confidence hits)]
                   ↓
        ┌─────────────────────┐
        │    STAGE 3:         │
        │    SYNTHESIS        │
        │ (Theme extraction,  │
        │  Contradiction ID,  │
        │  Gap analysis)      │
        └──────────┬──────────┘
                   ↓
        Research Report (JSON)
```

---

## Three-Stage Pipeline

### Stage 1: Quick Signal Check (2-3 seconds)
**Goal:** Is this query researchable? Is there initial signal?

**Sources (Fast + Free):**
- Wikipedia (summary + references)
- Google Scholar (metadata, no paywall check)
- GitHub (for code/technical topics)

**Strategy:**
- Parallel queries to all 3 sources
- Return top 20 results
- Filter by relevance > 0.6

**Success Criteria:**
- ≥2 high-confidence hits (confidence >= 0.8)
- Query deemed researchable

**Failure Outcome:**
- Exit pipeline; query not researchable with free sources

---

### Stage 2: Deep Research (5-10 seconds)
**Goal:** Find comprehensive, high-quality findings

**Sources (Domain-Specific):**
- **Biomedical:** PubMed, DOAJ (open access), Semantic Scholar
- **Computer Science:** arXiv, GitHub, Semantic Scholar
- **Physics/Math:** arXiv
- **General:** Google Scholar, Semantic Scholar, DOAJ
- **Philosophy:** Stanford Encyclopedia of Philosophy (SEP), DOAJ

**Strategy:**
- Only run if Stage 1 found signal
- Select 3-5 sources based on detected domain
- Query in parallel
- Early exit when saturation reached (15+ high-confidence hits)
- Remove duplicates from Stage 1

**Success Criteria:**
- ≥10 high-confidence unique hits, OR
- Saturation reached

---

### Stage 3: Synthesis & Extraction (1-2 seconds)
**Goal:** Extract structured intelligence

**Operations:**
1. **Theme Extraction** — Common concepts across top 10 hits
2. **Contradiction Identification** — Where sources disagree
3. **Confidence Aggregation** — Overall reliability score
4. **Gap Analysis** — What wasn't covered
5. **Next Steps** — Recommended follow-up research

---

## Source Tier System

**Tier 1 — GOLD (95% confidence)**
- PubMed (peer-reviewed biomedical)
- arXiv (preprints from researchers)
- Stanford Encyclopedia of Philosophy (expert-reviewed)

**Tier 2 — SILVER (80% confidence)**
- Google Scholar (aggregates academia)
- Semantic Scholar (AI-enhanced indexing)
- DOAJ (open-access journals)

**Tier 3 — BRONZE (65% confidence)**
- Wikipedia (crowd-sourced, good for overviews)
- GitHub (code-based knowledge)
- Medium (practitioner essays)

**Tier 4 — WEB (50% confidence)**
- News sites
- Blogs
- General web

---

## Domain Auto-Detection

Pipeline infers research domain from query keywords:

| Domain | Keywords | Primary Source |
|--------|----------|-----------------|
| **Biomedical** | disease, drug, treatment, protein, covid | PubMed |
| **Computer Science** | algorithm, ML, neural network, code | arXiv, GitHub |
| **Physics/Math** | quantum, particle, theorem, equation | arXiv |
| **Philosophy** | ethics, metaphysics, kant, plato | SEP |
| **History** | ancient, medieval, historical, war | Wikipedia, archives |
| **General** | (default) | Google Scholar, Semantic Scholar |

---

## Efficiency Features

### 1. Progressive Deepening (Don't search everywhere at once)
```
Query
  ↓
Stage 1: Search fast sources (2s) → Found good signal?
  ↓ YES
Stage 2: Search deep sources (8s) → Found enough?
  ↓ YES
Stage 3: Synthesis (1s)
  ↓
DONE (11s total vs 60s of sequential searching)
```

### 2. Early Exits (Stop when done)
- If Stage 1 finds no signal → Exit (query not researchable)
- If Stage 2 reaches saturation (15+ hits) → Skip remaining sources
- If confidence aggregate > 0.9 → No need to continue

### 3. Parallelization (Run simultaneously)
- All sources in a stage query in parallel
- WebSearch handles concurrency transparently
- Total time = slowest source, not sum of all

### 4. Deduplication (Avoid wasted queries)
- Track URLs across all results
- Don't report same paper twice
- Remove Stage 1 hits from Stage 2 results

### 5. Relevance Filtering (Skip noise)
- All hits filtered by relevance_score > 0.6
- Prevents low-quality results cluttering output
- Confidence score already weights by source tier

---

## Data Schema

### Research Hit
```python
{
  "source": "PubMed",           # Which source found it
  "title": "Study on X",
  "url": "https://...",
  "relevance_score": 0.85,      # 0-1, how relevant to query
  "confidence": 0.95,           # 0-1, source reliability
  "abstract": "...",
  "key_concepts": ["tag1", "tag2"],
  "publication_date": "2024-06-15",
  "citations": 42,              # How many other papers cite this
  "full_text_available": true
}
```

### Research Report
```python
{
  "query": "user's search",
  "domain": "computer_science",
  "timestamp": "2024-07-20T...",
  
  "summary": {
    "total_hits": 45,
    "high_confidence_hits": 18,
    "overall_confidence": 0.82
  },
  
  "top_findings": [
    # Ranked by relevance × confidence
  ],
  
  "key_themes": ["theme1", "theme2", "theme3"],
  "contradictions": [
    {
      "claim": "Source A says X",
      "contradiction": "Source B says not-X",
      "resolution": "Context-dependent"
    }
  ],
  
  "gaps": [
    "No data on newer methods",
    "Limited cross-domain analysis"
  ],
  
  "next_research_steps": [
    "Search for: [specific gap]",
    "Look into: [adjacent topic]"
  ]
}
```

---

## Integration Points

### 1. Claude Code WebSearch + WebFetch
```python
# For each query:
response = WebSearch(query=search_query, max_results=10)
for result in response.results:
    if result.url not in seen:
        full_text = WebFetch(url=result.url)
        extract_hit_from_text(full_text)
```

### 2. API Calls (Semantic Scholar, arXiv)
```python
# Free API, no key needed
response = requests.get(
    "https://api.semanticscholar.org/graph/v1/paper/search",
    params={"query": query}
)
```

### 3. Wikipedia API
```python
# Standard Wikipedia search API
response = requests.get(
    "https://en.wikipedia.org/w/api.php",
    params={"action": "query", "list": "search", "srsearch": query}
)
```

---

## Usage Examples

### Basic Research
```python
pipeline = ResearchPipeline()
report = pipeline.execute("machine learning in medicine")

print(report.confidence_overall)  # 0.82
print(report.top_findings[:3])    # Top 3 hits
print(report.key_themes)          # ["neural networks", "diagnosis", ...]
```

### Domain-Specific Research
```python
report = pipeline.execute(
    "quantum entanglement",
    domain=ResearchDomain.PHYSICS_MATH
)
# Automatically queries arXiv instead of PubMed
```

### Research with Constraints
```python
# Research only high-confidence sources (Tier 1-2)
pipeline.MIN_CONFIDENCE = 0.75
report = pipeline.execute("consciousness theories")
```

### Feeding into Wisdom System
```python
# Research a concept, then find matching teachings
pipeline = ResearchPipeline()
research_report = pipeline.execute("addiction neuroscience")

guidance_engine = ConsciousnessGuidanceEngine(...)
guidance = guidance_engine.query(level=50)  # Fear/addiction

# Cross-reference: research findings + wisdom teachings
combined = {
    "research": research_report.top_findings[:5],
    "wisdom": guidance.primary_teaching,
    "evidence_grade": "Research-informed teaching"
}
```

---

## Performance Expectations

| Stage | Time | Sources | Hits | Quality |
|-------|------|---------|------|---------|
| Stage 1 | 2-3s | 3 | 6-20 | 60% signal |
| Stage 2 | 5-8s | 3-5 | 20-50 | 90% signal |
| Stage 3 | 1s | — | Synthesized | 95% confidence |
| **Total** | **8-12s** | **6-8** | **20-50** | **High** |

**vs. Manual Research:** 60+ seconds per source × 6-8 sources = 360-480 seconds (no synthesis)

**Speedup:** 30-50x faster than sequential; 5x faster than parallel manual search

---

## Limitations & Future Enhancements

### Current Limitations
- Free sources only (some paywall content excluded)
- No full-text PDF extraction (copyright issues)
- Domain detection based on keywords (could use ML)
- No API keys used (rate-limited by source)
- Synthesis is pattern-based (not AI-generated)

### Future Enhancements
- **ML-powered domain classification** (higher accuracy)
- **Semantic similarity** (group related papers, avoid duplicates)
- **Citation graph traversal** (find seminal works)
- **Temporal filtering** (recent papers vs foundational)
- **Author reputation scoring** (h-index integration)
- **Full-text integration** (extract key passages)
- **Multi-language support** (non-English sources)
- **Custom source plugins** (extensible architecture)

---

## Integration with HumanAIOS Ecosystem

### Research → Guidance Loop
```
Research Pipeline
    ↓ (research_report)
Consciousness Guidance Engine
    ↓ (wisdom_teachings)
Obstacle-to-Opportunity Translator
    ↓ (reframed_insights)
User Application
```

### Example Workflow
1. User queries: "I struggle with addictive thoughts"
2. Research Pipeline searches for addiction neuroscience
3. Guidance Engine returns AA Step 1 + Buddhist parallels
4. Obstacle Translator shows: "Addiction = doorway to Step 1"
5. User gets: [Research findings] + [Wisdom teaching] + [Reframing]

---

## Technical Stack

**Core:** Python 3.10+
**External APIs:** 
- WebSearch/WebFetch (Claude Code)
- Semantic Scholar API (free, no auth)
- Wikipedia API (free, no auth)
- arXiv API (free, no auth)

**Dependencies:** requests, json, dataclasses, enum

---

## Deployment Checklist

- [ ] WebSearch integration tested
- [ ] WebFetch integration tested
- [ ] All 8 sources callable
- [ ] Rate limiting handled
- [ ] Error recovery implemented
- [ ] JSON serialization working
- [ ] Stage gates functioning
- [ ] Deduplication logic verified
- [ ] Performance benchmarked
- [ ] Documentation complete

---

## Philosophy

**Automated research should:**
1. Be fast (seconds, not minutes)
2. Be comprehensive (multiple sources, not just one)
3. Be intelligent (domain-aware source selection)
4. Be actionable (structured output, not raw results)
5. Know when to stop (saturation detection, early exits)

**This pipeline embodies all five principles.**

---

*Design: 2026-07-20*  
*Status: Ready for WebSearch/WebFetch integration*  
*Next: Test with real queries and refine source selection*
