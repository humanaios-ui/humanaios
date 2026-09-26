# Composite Utilization Ranking — pre-registered v1.0
# Locked prior to metric collection. Session 2026-08-22.
# score(repo) = 0.40*N1 + 0.35*N2 + 0.25*N3
#   C1 = commits authored by humanaios-ui in repo (all-time, via API author filter)
#   C2 = mention count of repo name in live REGISTERED.md (pinned this session)
#   C3 = recency = 1 / (1 + days_since_last_push)
#   N1..N3 = min-max normalization of C1..C3 across all 90 repos
# Tie-break: higher C1 wins; then non-fork over fork.
# Exclusions: none. Forks eligible but scored on authored commits only.
