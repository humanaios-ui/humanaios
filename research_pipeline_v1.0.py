#!/usr/bin/env python3
"""
Automated Research Pipeline Engine v1.0

Orchestrates efficient research across free sources with parallel querying,
progressive filtering, and structured output.

Architecture:
- Stage 1 (Quick Signal): Google Scholar, Wikipedia, GitHub (fast, cheap)
- Gate 1 (Relevance Filter): Skip if no signal found
- Stage 2 (Deep Research): PubMed, arXiv, Open Access journals (selective)
- Gate 2 (Quality Filter): Aggregate and verify findings
- Stage 3 (Synthesis): Extract structured insights, identify gaps

Pipeline Strategy: Progressive deepening with early exits
"""

import json
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple, Set
from enum import Enum
from datetime import datetime


class ResearchDomain(Enum):
    """Research topic domains (affects source selection)"""
    BIOMEDICAL = "biomedical"  # PubMed, MEDLINE
    COMPUTER_SCIENCE = "computer_science"  # arXiv, GitHub
    PHYSICS_MATH = "physics_math"  # arXiv primarily
    GENERAL = "general"  # Wikipedia, Google Scholar
    BUSINESS = "business"  # News, business journals
    HISTORY = "history"  # Historical texts, archives
    PHILOSOPHY = "philosophy"  # Stanford Encyclopedia, SEP


class SourceTier(Enum):
    """Source reliability tiers"""
    TIER_1_GOLD = (0.95, ["PubMed", "arXiv", "Stanford Encyclopedia"])
    TIER_2_SILVER = (0.80, ["Google Scholar", "Open Access Journals", "Semantic Scholar"])
    TIER_3_BRONZE = (0.65, ["Wikipedia", "Medium", "GitHub"])
    TIER_4_WEB = (0.50, ["News sites", "Blogs", "General web"])


@dataclass
class ResearchSource:
    """A potential research source"""
    name: str
    tier: SourceTier
    url_pattern: str
    search_format: str  # How to construct search URL
    supports_domains: List[ResearchDomain]
    cost: str  # "free", "free_with_limits", "paid"
    extraction_method: str  # How to extract data (html_parse, json_api, etc.)
    parallelizable: bool = True


@dataclass
class ResearchHit:
    """A single research finding"""
    source: str
    title: str
    url: str
    relevance_score: float  # 0-1, how relevant to query
    confidence: float  # 0-1, how reliable the source is
    abstract: Optional[str] = None
    key_concepts: Optional[List[str]] = None
    publication_date: Optional[str] = None
    citations: Optional[int] = None
    full_text_available: bool = False


@dataclass
class ResearchPhaseResult:
    """Result from one pipeline phase"""
    phase_name: str
    hits: List[ResearchHit]
    total_sources_queried: int
    high_confidence_count: int  # Hits with confidence >= 0.8
    execution_time_seconds: float
    reached_saturation: bool  # True if found enough signal to stop


@dataclass
class ResearchReport:
    """Final research output"""
    query: str
    domain: ResearchDomain
    timestamp: str
    phase_results: List[ResearchPhaseResult]

    # Synthesis layer
    top_findings: List[ResearchHit]
    key_themes: List[str]
    contradictions: List[Dict]  # Where sources disagree
    confidence_overall: float  # Aggregate confidence
    gaps_identified: List[str]  # What wasn't found
    next_research_steps: List[str]  # Recommended follow-ups

    def to_dict(self):
        return {
            "query": self.query,
            "domain": self.domain.value,
            "timestamp": self.timestamp,
            "summary": {
                "total_hits": sum(len(p.hits) for p in self.phase_results),
                "high_confidence_hits": sum(p.high_confidence_count for p in self.phase_results),
                "phases_completed": len(self.phase_results),
                "overall_confidence": self.confidence_overall,
            },
            "top_findings": [
                {
                    "source": h.source,
                    "title": h.title,
                    "url": h.url,
                    "relevance": h.relevance_score,
                    "confidence": h.confidence,
                }
                for h in self.top_findings[:10]
            ],
            "key_themes": self.key_themes,
            "contradictions": self.contradictions,
            "gaps": self.gaps_identified,
            "next_steps": self.next_research_steps,
        }


class ResearchPipeline:
    """Main research orchestration engine"""

    # Source definitions (free sources only)
    SOURCES = {
        "google_scholar": ResearchSource(
            name="Google Scholar",
            tier=SourceTier.TIER_2_SILVER,
            url_pattern="https://scholar.google.com/scholar",
            search_format="q={query}",
            supports_domains=[ResearchDomain.GENERAL, ResearchDomain.COMPUTER_SCIENCE],
            cost="free",
            extraction_method="html_parse",
            parallelizable=True,
        ),
        "pubmed": ResearchSource(
            name="PubMed",
            tier=SourceTier.TIER_1_GOLD,
            url_pattern="https://pubmed.ncbi.nlm.nih.gov/",
            search_format="?term={query}",
            supports_domains=[ResearchDomain.BIOMEDICAL],
            cost="free",
            extraction_method="json_api",
            parallelizable=True,
        ),
        "arxiv": ResearchSource(
            name="arXiv",
            tier=SourceTier.TIER_1_GOLD,
            url_pattern="https://arxiv.org/search",
            search_format="?query={query}&searchtype=all",
            supports_domains=[ResearchDomain.COMPUTER_SCIENCE, ResearchDomain.PHYSICS_MATH],
            cost="free",
            extraction_method="json_api",
            parallelizable=True,
        ),
        "wikipedia": ResearchSource(
            name="Wikipedia",
            tier=SourceTier.TIER_3_BRONZE,
            url_pattern="https://en.wikipedia.org/w/api.php",
            search_format="?action=query&list=search&srsearch={query}",
            supports_domains=[ResearchDomain.GENERAL, ResearchDomain.HISTORY, ResearchDomain.PHILOSOPHY],
            cost="free",
            extraction_method="json_api",
            parallelizable=True,
        ),
        "github": ResearchSource(
            name="GitHub",
            tier=SourceTier.TIER_3_BRONZE,
            url_pattern="https://api.github.com/search/repositories",
            search_format="?q={query}",
            supports_domains=[ResearchDomain.COMPUTER_SCIENCE],
            cost="free",
            extraction_method="json_api",
            parallelizable=True,
        ),
        "semantic_scholar": ResearchSource(
            name="Semantic Scholar",
            tier=SourceTier.TIER_2_SILVER,
            url_pattern="https://api.semanticscholar.org/graph/v1/paper/search",
            search_format="?query={query}",
            supports_domains=[ResearchDomain.GENERAL, ResearchDomain.BIOMEDICAL, ResearchDomain.COMPUTER_SCIENCE],
            cost="free",
            extraction_method="json_api",
            parallelizable=True,
        ),
        "doaj": ResearchSource(
            name="DOAJ (Open Access Journals)",
            tier=SourceTier.TIER_2_SILVER,
            url_pattern="https://doaj.org/api/v3/search/articles",
            search_format="?q={query}",
            supports_domains=[ResearchDomain.GENERAL, ResearchDomain.BIOMEDICAL],
            cost="free",
            extraction_method="json_api",
            parallelizable=True,
        ),
    }

    # Constants
    RELEVANCE_THRESHOLD = 0.6  # Skip hits below this
    HIGH_CONFIDENCE_THRESHOLD = 0.8
    SATURATION_POINT = 15  # If we have 15+ high-confidence hits, stop searching
    PHASE_TIMEOUT = 30  # seconds

    def __init__(self):
        """Initialize pipeline"""
        self.phase_results = []
        self.all_hits: Set[str] = set()  # Track URLs to avoid duplicates

    def detect_domain(self, query: str) -> ResearchDomain:
        """Infer research domain from query"""
        query_lower = query.lower()

        # Simple heuristics (could be enhanced with ML)
        if any(word in query_lower for word in ["covid", "disease", "treatment", "drug", "medical", "protein"]):
            return ResearchDomain.BIOMEDICAL
        elif any(word in query_lower for word in ["algorithm", "neural network", "machine learning", "software", "code"]):
            return ResearchDomain.COMPUTER_SCIENCE
        elif any(word in query_lower for word in ["quantum", "relativity", "particle", "wave equation", "theorem"]):
            return ResearchDomain.PHYSICS_MATH
        elif any(word in query_lower for word in ["ancient", "medieval", "historical", "war", "civilization"]):
            return ResearchDomain.HISTORY
        elif any(word in query_lower for word in ["philosophy", "kant", "plato", "ethics", "metaphysics"]):
            return ResearchDomain.PHILOSOPHY
        else:
            return ResearchDomain.GENERAL

    def select_sources_for_domain(self, domain: ResearchDomain) -> List[str]:
        """Select best sources for detected domain"""
        eligible = []
        for source_key, source in self.SOURCES.items():
            if domain in source.supports_domains:
                eligible.append(source_key)

        # Sort by tier (gold first)
        def tier_rank(key):
            tier_val = self.SOURCES[key].tier.value[0]
            return -tier_val  # Negative so higher confidence sorts first

        return sorted(eligible, key=tier_rank)

    def stage_1_quick_signal(self, query: str, domain: ResearchDomain) -> ResearchPhaseResult:
        """
        Stage 1: Quick Signal Check
        Search fast, cheap sources (Wikipedia, Google Scholar)
        Goal: Determine if query is researchable and find initial signal
        """
        print(f"\n[STAGE 1] Quick Signal Check for: {query}")

        # Select quick sources (Wikipedia, Google Scholar)
        quick_sources = ["wikipedia", "google_scholar"]

        hits = []
        sources_queried = 0

        # Simulate searching (in real implementation, would use WebSearch/WebFetch)
        for source_key in quick_sources:
            if source_key in self.SOURCES:
                source = self.SOURCES[source_key]
                sources_queried += 1

                # Mock results (in practice: call WebSearch/WebFetch)
                mock_hits = self._mock_search(source, query, domain)
                hits.extend(mock_hits)

        # Filter by relevance
        hits = [h for h in hits if h.relevance_score >= self.RELEVANCE_THRESHOLD]

        high_conf = len([h for h in hits if h.confidence >= self.HIGH_CONFIDENCE_THRESHOLD])
        reached_sat = high_conf >= 5  # Low bar for Stage 1

        result = ResearchPhaseResult(
            phase_name="Quick Signal",
            hits=hits[:20],  # Limit results
            total_sources_queried=sources_queried,
            high_confidence_count=high_conf,
            execution_time_seconds=2.1,  # Mock
            reached_saturation=reached_sat,
        )

        print(f"  Found {len(hits)} hits ({high_conf} high-confidence)")
        print(f"  Saturation reached: {reached_sat}")

        return result

    def stage_2_deep_research(self, query: str, domain: ResearchDomain, stage_1_result: ResearchPhaseResult) -> ResearchPhaseResult:
        """
        Stage 2: Deep Research
        Only run if Stage 1 found signal. Search domain-specific sources (PubMed, arXiv, Semantic Scholar)
        Goal: Find comprehensive, high-quality findings
        """
        print(f"\n[STAGE 2] Deep Research")

        # Early exit if no signal
        if stage_1_result.high_confidence_count < 2:
            print("  Early exit: Insufficient signal from Stage 1")
            return ResearchPhaseResult(
                phase_name="Deep Research",
                hits=[],
                total_sources_queried=0,
                high_confidence_count=0,
                execution_time_seconds=0,
                reached_saturation=False,
            )

        # Select deep sources based on domain
        deep_sources = self.select_sources_for_domain(domain)
        # Filter to gold/silver tier only
        deep_sources = [s for s in deep_sources if s not in ["wikipedia", "google_scholar"]]

        hits = []
        sources_queried = 0

        for source_key in deep_sources:
            if source_key in self.SOURCES:
                source = self.SOURCES[source_key]
                sources_queried += 1

                mock_hits = self._mock_search(source, query, domain)
                hits.extend(mock_hits)

                # Early exit if we've reached saturation
                high_conf = len([h for h in hits if h.confidence >= self.HIGH_CONFIDENCE_THRESHOLD])
                if high_conf >= self.SATURATION_POINT:
                    print(f"  Saturation reached after {source.name}")
                    break

        # Remove duplicates from Stage 1
        stage_1_urls = {h.url for h in stage_1_result.hits}
        hits = [h for h in hits if h.url not in stage_1_urls]

        # Filter by relevance
        hits = [h for h in hits if h.relevance_score >= self.RELEVANCE_THRESHOLD]

        high_conf = len([h for h in hits if h.confidence >= self.HIGH_CONFIDENCE_THRESHOLD])
        reached_sat = high_conf >= self.SATURATION_POINT

        result = ResearchPhaseResult(
            phase_name="Deep Research",
            hits=hits[:30],
            total_sources_queried=sources_queried,
            high_confidence_count=high_conf,
            execution_time_seconds=8.3,  # Mock
            reached_saturation=reached_sat,
        )

        print(f"  Found {len(hits)} unique hits ({high_conf} high-confidence)")

        return result

    def stage_3_synthesis(self, query: str, all_results: List[ResearchPhaseResult]) -> Dict:
        """
        Stage 3: Synthesis & Extraction
        Extract structured insights, identify themes and contradictions
        """
        print(f"\n[STAGE 3] Synthesis & Extraction")

        # Aggregate all hits
        all_hits = []
        for phase in all_results:
            all_hits.extend(phase.hits)

        # Sort by relevance and confidence
        all_hits = sorted(all_hits, key=lambda h: (h.relevance_score * 0.6 + h.confidence * 0.4), reverse=True)

        # Extract themes from top hits
        themes = self._extract_themes(all_hits[:10])

        # Identify contradictions (mock)
        contradictions = self._identify_contradictions(all_hits)

        # Calculate overall confidence
        if all_hits:
            overall_conf = sum(h.confidence for h in all_hits) / len(all_hits)
        else:
            overall_conf = 0

        # Identify gaps
        gaps = self._identify_gaps(query, themes)

        # Suggest next steps
        next_steps = self._suggest_next_steps(query, gaps)

        return {
            "all_hits": all_hits,
            "themes": themes,
            "contradictions": contradictions,
            "confidence": overall_conf,
            "gaps": gaps,
            "next_steps": next_steps,
        }

    def execute(self, query: str, domain: Optional[ResearchDomain] = None) -> ResearchReport:
        """
        Execute full research pipeline
        """
        print(f"\n{'='*70}")
        print(f"AUTOMATED RESEARCH PIPELINE | Query: {query}")
        print(f"{'='*70}")

        # Detect domain if not specified
        if domain is None:
            domain = self.detect_domain(query)
            print(f"Detected domain: {domain.value}")

        # Stage 1: Quick Signal
        phase_1 = self.stage_1_quick_signal(query, domain)
        self.phase_results.append(phase_1)

        # Gate 1: Check if we found signal
        if phase_1.high_confidence_count == 0:
            print("\n⚠ Gate 1 Failed: No signal found. Terminating pipeline.")
            return self._create_report(query, domain)

        # Stage 2: Deep Research
        phase_2 = self.stage_2_deep_research(query, domain, phase_1)
        self.phase_results.append(phase_2)

        # Stage 3: Synthesis
        synthesis = self.stage_3_synthesis(query, self.phase_results)

        # Create final report
        report = ResearchReport(
            query=query,
            domain=domain,
            timestamp=datetime.now().isoformat(),
            phase_results=self.phase_results,
            top_findings=synthesis["all_hits"][:10],
            key_themes=synthesis["themes"],
            contradictions=synthesis["contradictions"],
            confidence_overall=synthesis["confidence"],
            gaps_identified=synthesis["gaps"],
            next_research_steps=synthesis["next_steps"],
        )

        print(f"\n{'='*70}")
        print(f"RESEARCH COMPLETE")
        print(f"Total hits found: {len(synthesis['all_hits'])}")
        print(f"Overall confidence: {synthesis['confidence']:.2f}")
        print(f"{'='*70}\n")

        return report

    # Helper methods
    def _mock_search(self, source: ResearchSource, query: str, domain: ResearchDomain) -> List[ResearchHit]:
        """Mock search results (replace with actual WebSearch/WebFetch)"""
        # Return sample hits for demonstration
        return [
            ResearchHit(
                source=source.name,
                title=f"Research on {query}",
                url=f"{source.url_pattern}/result1",
                relevance_score=0.85,
                confidence=source.tier.value[0],
                abstract="Finding abstract here",
                key_concepts=["concept1", "concept2"],
                publication_date="2024-06-15",
                citations=42,
            ),
            ResearchHit(
                source=source.name,
                title=f"Study of {query} implications",
                url=f"{source.url_pattern}/result2",
                relevance_score=0.72,
                confidence=source.tier.value[0],
                abstract="Another finding",
                key_concepts=["aspect1", "aspect2"],
                publication_date="2024-05-20",
                citations=18,
            ),
        ]

    def _extract_themes(self, hits: List[ResearchHit]) -> List[str]:
        """Extract common themes from top hits"""
        all_concepts = []
        for hit in hits:
            if hit.key_concepts:
                all_concepts.extend(hit.key_concepts)

        # Return most common (mock)
        return list(set(all_concepts))[:5] if all_concepts else ["theme1", "theme2"]

    def _identify_contradictions(self, hits: List[ResearchHit]) -> List[Dict]:
        """Identify where sources disagree"""
        # Mock implementation
        return [
            {
                "claim": "Source A says X",
                "contradiction": "Source B says not-X",
                "resolution": "Context-dependent based on study design",
            }
        ]

    def _identify_gaps(self, query: str, themes: List[str]) -> List[str]:
        """Identify what wasn't covered"""
        return [
            f"No findings on {query} + advanced methodology",
            f"Limited data on cross-domain applications",
            f"Recent developments (post-2024) not fully captured",
        ]

    def _suggest_next_steps(self, query: str, gaps: List[str]) -> List[str]:
        """Suggest follow-up research"""
        return [
            f"Deep-dive into: {gaps[0] if gaps else 'methodology'}",
            f"Cross-reference with adjacent domains",
            f"Search for preprints and working papers (arXiv)",
            f"Contact domain experts for primary research",
        ]

    def _create_report(self, query: str, domain: ResearchDomain) -> ResearchReport:
        """Create empty report when pipeline terminates early"""
        return ResearchReport(
            query=query,
            domain=domain,
            timestamp=datetime.now().isoformat(),
            phase_results=self.phase_results,
            top_findings=[],
            key_themes=[],
            contradictions=[],
            confidence_overall=0,
            gaps_identified=["Query not researchable with available sources"],
            next_research_steps=["Revise query", "Try different keywords"],
        )


# ============================================================================
# TEST CASES
# ============================================================================

def run_test_research():
    """Run test research queries"""
    print("\n" + "=" * 70)
    print("AUTOMATED RESEARCH PIPELINE - TEST SUITE")
    print("=" * 70)

    pipeline = ResearchPipeline()

    test_queries = [
        {"query": "machine learning in medical imaging", "domain": ResearchDomain.COMPUTER_SCIENCE},
        {"query": "consciousness and neural correlates", "domain": ResearchDomain.BIOMEDICAL},
        {"query": "ancient stoic philosophy", "domain": ResearchDomain.PHILOSOPHY},
    ]

    for test in test_queries:
        print(f"\n{'—' * 70}")
        print(f"QUERY: {test['query']}")
        print(f"{'—' * 70}")

        try:
            report = pipeline.execute(test["query"], test["domain"])

            # Print summary
            print("\nRESEARCH SUMMARY:")
            print(f"  Domain: {report.domain.value}")
            print(f"  Confidence: {report.confidence_overall:.2f}")
            print(f"  Themes: {', '.join(report.key_themes[:3])}")
            print(f"  Gaps: {report.gaps_identified[0] if report.gaps_identified else 'None'}")

            print(f"\nTOP FINDINGS:")
            for i, hit in enumerate(report.top_findings[:3], 1):
                print(f"  {i}. {hit.title} ({hit.source})")

            print(f"\nNEXT STEPS:")
            for step in report.next_research_steps[:2]:
                print(f"  • {step}")

        except Exception as e:
            print(f"ERROR: {e}")


if __name__ == "__main__":
    run_test_research()
