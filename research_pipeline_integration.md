# Research Pipeline Integration Guide
## Connecting to Real Free Sources

---

## Quick Start: How to Use the Pipeline

```python
from research_pipeline_v1 import ResearchPipeline, ResearchDomain

# Initialize
pipeline = ResearchPipeline()

# Execute research
report = pipeline.execute("machine learning in medical imaging")

# Access results
print(f"Confidence: {report.confidence_overall}")
print(f"Top findings: {len(report.top_findings)}")
print(f"Themes: {report.key_themes}")
print(f"Next steps: {report.next_research_steps}")

# Export
json_data = report.to_dict()
```

---

## Free Sources Reference

### 1. **PubMed (Biomedical)**

**URL:** https://pubmed.ncbi.nlm.nih.gov/

**API:** https://www.ncbi.nlm.nih.gov/research/pubtator-api/

**Free Tier:** Yes, unlimited (no API key needed)

**How to Query:**
```bash
# Web search
https://pubmed.ncbi.nlm.nih.gov/?term=machine+learning+medical

# API (JSON)
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=query&rettype=json&retmax=10
```

**Implementation:**
```python
import requests

def search_pubmed(query, max_results=10):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "rettype": "json",
        "retmax": max_results
    }
    response = requests.get(url, params=params)
    return response.json()
```

---

### 2. **arXiv (Physics, CS, Math)**

**URL:** https://arxiv.org/

**API:** https://arxiv.org/help/api/

**Free Tier:** Yes, unlimited (rate limit: 3 requests per second)

**How to Query:**
```bash
# API (Atom/XML)
https://export.arxiv.org/api/query?search_query=cat:cs.AI+AND+submittedDate:[202401010000+TO+202412312359]&start=0&max_results=10
```

**Implementation:**
```python
import requests
import xml.etree.ElementTree as ET

def search_arxiv(query, max_results=10):
    url = "https://export.arxiv.org/api/query"
    params = {
        "search_query": query,
        "max_results": max_results
    }
    response = requests.get(url, params=params)
    root = ET.fromstring(response.content)
    
    results = []
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        url = entry.find('{http://www.w3.org/2005/Atom}id').text
        results.append({"title": title, "url": url})
    
    return results
```

---

### 3. **Semantic Scholar (AI-Enhanced Research)**

**URL:** https://www.semanticscholar.org/

**API:** https://api.semanticscholar.org/

**Free Tier:** Yes, 100 requests per 5 minutes (no key needed)

**How to Query:**
```bash
# API (JSON)
https://api.semanticscholar.org/graph/v1/paper/search?query=neural+networks+medicine
```

**Implementation:**
```python
def search_semantic_scholar(query, max_results=10):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": max_results
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    results = []
    for paper in data.get("data", []):
        results.append({
            "title": paper["title"],
            "url": f"https://www.semanticscholar.org/paper/{paper['paperId']}",
            "citations": paper.get("citationCount", 0),
            "abstract": paper.get("abstract", "")
        })
    
    return results
```

---

### 4. **Wikipedia (General Reference)**

**URL:** https://en.wikipedia.org/

**API:** https://en.wikipedia.org/w/api.php

**Free Tier:** Yes, unlimited

**How to Query:**
```bash
# API (JSON)
https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=machine+learning&format=json
```

**Implementation:**
```python
def search_wikipedia(query, max_results=5):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": max_results,
        "format": "json"
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    results = []
    for item in data["query"]["search"]:
        title = item["title"]
        snippet = item["snippet"]
        results.append({
            "title": title,
            "url": f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
            "snippet": snippet
        })
    
    return results
```

---

### 5. **Google Scholar (Aggregated Research)**

**URL:** https://scholar.google.com/

**API:** No official API (rate-limited by Google)

**Alternative:** Use Scholar.Py or Scholarly

**Implementation:**
```python
# Using scholarly library (pip install scholarly)
from scholarly import scholarly

def search_google_scholar(query, max_results=10):
    search_query = scholarly.search_pubs(query)
    
    results = []
    for i, pub in enumerate(search_query):
        if i >= max_results:
            break
        results.append({
            "title": pub.get("title", ""),
            "url": pub.get("url", ""),
            "year": pub.get("pub_year", ""),
            "citations": pub.get("num_citations", 0)
        })
    
    return results
```

---

### 6. **DOAJ (Open Access Journals)**

**URL:** https://doaj.org/

**API:** https://doaj.org/api/v3/

**Free Tier:** Yes, unlimited (rate limit: 3600 per hour)

**How to Query:**
```bash
# API (JSON)
https://doaj.org/api/v3/search/articles?q=machine+learning
```

**Implementation:**
```python
def search_doaj(query, max_results=10):
    url = "https://doaj.org/api/v3/search/articles"
    params = {
        "q": query,
        "pageSize": max_results
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    results = []
    for article in data.get("results", []):
        bibjson = article.get("bibjson", {})
        results.append({
            "title": bibjson.get("title", ""),
            "url": bibjson.get("link", [{}])[0].get("url", ""),
            "journal": bibjson.get("journal", {}).get("title", ""),
            "year": bibjson.get("year", "")
        })
    
    return results
```

---

### 7. **GitHub (Code + Documentation)**

**URL:** https://github.com/

**API:** https://api.github.com/

**Free Tier:** Yes, 60 requests per hour (authenticated: 5000/hour)

**How to Query:**
```bash
# API (JSON)
https://api.github.com/search/repositories?q=neural+networks&sort=stars
```

**Implementation:**
```python
def search_github(query, max_results=10):
    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "per_page": max_results,
        "sort": "stars"
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    results = []
    for repo in data.get("items", []):
        results.append({
            "title": repo["name"],
            "url": repo["html_url"],
            "description": repo["description"],
            "stars": repo["stargazers_count"],
            "language": repo["language"]
        })
    
    return results
```

---

### 8. **Stanford Encyclopedia of Philosophy**

**URL:** https://plato.stanford.edu/

**API:** No official API (scrape titles/URLs)

**Implementation:**
```python
def search_sep(query):
    # Limited - would need scraping
    # Returns matching article titles from known articles
    # Better: use their search page
    url = f"https://plato.stanford.edu/search/searcher.py?query={query}"
    # This returns HTML - would need parsing
    return []
```

---

## Putting It Together: Full Pipeline Implementation

```python
import asyncio
import requests
from typing import List, Dict

class ResearchPipelineIntegrated:
    """Production pipeline with real sources"""
    
    def __init__(self):
        self.sources = {
            "wikipedia": self.search_wikipedia,
            "google_scholar": self.search_google_scholar,
            "pubmed": self.search_pubmed,
            "arxiv": self.search_arxiv,
            "semantic_scholar": self.search_semantic_scholar,
            "doaj": self.search_doaj,
            "github": self.search_github,
        }
    
    async def search_all_parallel(self, query: str, sources: List[str]) -> Dict[str, List]:
        """Search multiple sources in parallel"""
        tasks = []
        
        for source_name in sources:
            if source_name in self.sources:
                task = asyncio.create_task(
                    self._async_search(source_name, query)
                )
                tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        output = {}
        for source_name, result in zip(sources, results):
            if isinstance(result, Exception):
                output[source_name] = []
            else:
                output[source_name] = result
        
        return output
    
    async def _async_search(self, source_name: str, query: str):
        """Wrapper for async execution"""
        return self.sources[source_name](query)
    
    def search_wikipedia(self, query: str, max_results=5):
        """See implementation above"""
        # ... code here
        pass
    
    def search_google_scholar(self, query: str, max_results=10):
        """See implementation above"""
        # ... code here
        pass
    
    def search_pubmed(self, query: str, max_results=10):
        """See implementation above"""
        # ... code here
        pass
    
    # ... other search methods
    
    def execute_research(self, query: str, domain: str = "general"):
        """Execute full pipeline"""
        # Stage 1: Quick signal
        stage_1_sources = ["wikipedia", "google_scholar"]
        stage_1_results = asyncio.run(
            self.search_all_parallel(query, stage_1_sources)
        )
        
        # Check signal
        total_hits = sum(len(r) for r in stage_1_results.values())
        if total_hits < 2:
            return {"status": "no_signal", "message": "Query not researchable"}
        
        # Stage 2: Deep research
        stage_2_sources = self._select_deep_sources(domain)
        stage_2_results = asyncio.run(
            self.search_all_parallel(query, stage_2_sources)
        )
        
        # Combine and deduplicate
        all_results = {**stage_1_results, **stage_2_results}
        
        # Stage 3: Synthesis
        synthesis = self._synthesize(all_results, query)
        
        return synthesis
    
    def _select_deep_sources(self, domain: str) -> List[str]:
        """Select sources based on domain"""
        domain_sources = {
            "biomedical": ["pubmed", "semantic_scholar", "doaj"],
            "computer_science": ["arxiv", "github", "semantic_scholar"],
            "physics": ["arxiv"],
            "general": ["semantic_scholar", "doaj"],
            "philosophy": ["semantic_scholar"],
        }
        return domain_sources.get(domain, ["semantic_scholar"])
    
    def _synthesize(self, all_results: Dict, query: str) -> Dict:
        """Extract themes and structure output"""
        # Flatten results
        flat_results = []
        for source, hits in all_results.items():
            for hit in hits:
                hit["source"] = source
                flat_results.append(hit)
        
        # Deduplicate by URL
        seen_urls = set()
        unique_results = []
        for hit in flat_results:
            url = hit.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(hit)
        
        # Extract themes
        themes = self._extract_themes(unique_results)
        
        # Return report
        return {
            "query": query,
            "hits": unique_results[:20],
            "themes": themes,
            "total": len(unique_results),
            "confidence": 0.75,  # Mock
        }
    
    def _extract_themes(self, hits: List[Dict]) -> List[str]:
        """Extract common themes from hits"""
        # Simple implementation - count common words
        from collections import Counter
        
        words = []
        for hit in hits:
            title = hit.get("title", "").lower()
            words.extend(title.split())
        
        # Filter out common words
        stopwords = {"the", "a", "and", "or", "in", "of", "to", "is", "are"}
        words = [w for w in words if w not in stopwords and len(w) > 3]
        
        # Get most common
        common = Counter(words).most_common(5)
        return [word for word, count in common]

# Usage
pipeline = ResearchPipelineIntegrated()
report = pipeline.execute_research("machine learning in medicine", domain="biomedical")
print(report)
```

---

## Rate Limiting & Best Practices

### Rate Limits to Remember
| Source | Limit | Workaround |
|--------|-------|-----------|
| PubMed | Unlimited | Add delay between requests |
| arXiv | 3 req/sec | Queue requests |
| Semantic Scholar | 100 req/5min | Cache results |
| Wikipedia | Unlimited | Add user agent |
| Google Scholar | Anti-scraping | Use scholarly lib |
| DOAJ | 3600/hour | Monitor requests |
| GitHub | 60/hour (auth: 5000) | Use auth token |

### Best Practices
```python
# 1. Add delays
import time
time.sleep(0.5)  # Between requests

# 2. Use user agent
headers = {
    "User-Agent": "Mozilla/5.0 (Research Pipeline v1.0)"
}
requests.get(url, headers=headers)

# 3. Cache results
import json
cache = {}
cache_key = f"{source}_{query}"
if cache_key in cache:
    return cache[cache_key]

# 4. Handle errors gracefully
try:
    result = requests.get(url, timeout=10)
except requests.Timeout:
    return []  # Skip this source
```

---

## Testing Against Real Sources

```python
# Test each source individually
def test_sources():
    pipeline = ResearchPipelineIntegrated()
    query = "consciousness neuroscience"
    
    print("Testing Wikipedia...")
    wiki_results = pipeline.search_wikipedia(query)
    print(f"  ✓ Found {len(wiki_results)} results")
    
    print("Testing arXiv...")
    arxiv_results = pipeline.search_arxiv(query)
    print(f"  ✓ Found {len(arxiv_results)} results")
    
    print("Testing Semantic Scholar...")
    ss_results = pipeline.search_semantic_scholar(query)
    print(f"  ✓ Found {len(ss_results)} results")
    
    print("Testing PubMed...")
    pubmed_results = pipeline.search_pubmed(query)
    print(f"  ✓ Found {len(pubmed_results)} results")

test_sources()
```

---

## Next Steps

1. ✅ Architecture designed
2. ⏳ Real source implementations (partial above)
3. ⏳ Error handling & retries
4. ⏳ Caching layer
5. ⏳ Async/parallel execution verified
6. ⏳ Performance benchmarking
7. ⏳ Integration with wisdom system

---

*Integration Guide: 2026-07-20*  
*Status: Ready to implement with real sources*
