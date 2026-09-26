"""
M2 Rank 3 Phase 6: Registry Verification & Testing
Full test suite for entity registry consistency and cross-practice integration.

Status: Implementation (2026-08-13)
Objective: Validate entity registry with 16+ tests covering entities, relationships,
cross-practice integration, performance, and sync pipeline.
"""

import sqlite3
import os
import time
from pathlib import Path
from typing import List, Tuple, Any


class RegistryVerificationSuite:
    def __init__(self, db_path: str = "os.path.expanduser("~/.empirica/workspace/workspace.db")"):
        self.db_path = db_path
        try:
            self.db = sqlite3.connect(db_path)
            self.db.row_factory = sqlite3.Row
        except sqlite3.OperationalError as e:
            raise RuntimeError(f"Cannot connect to database at {db_path}: {e}")
        self.test_results = []

    def query(self, sql: str) -> List[Tuple[Any, ...]]:
        """Execute a query and return results"""
        cursor = self.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def query_one(self, sql: str) -> Any:
        """Execute a query and return single result"""
        result = self.query(sql)
        return result[0] if result else None

    def test_result(self, test_name: str, passed: bool, message: str = ""):
        """Record a test result"""
        status = "PASS" if passed else "FAIL"
        self.test_results.append({
            "name": test_name,
            "status": status,
            "message": message
        })
        symbol = "✓" if passed else "✗"
        print(f"  {symbol} {test_name}" + (f" — {message}" if message else ""))

    # ============================================================================
    # Entity Verification Tests (4 tests)
    # ============================================================================

    def test_all_entities_registered(self):
        """Verify all entities exist in registry"""
        try:
            projects = self.query_one(
                "SELECT COUNT(*) FROM entity_registry WHERE entity_type='project'"
            )
            contacts = self.query_one(
                "SELECT COUNT(*) FROM entity_registry WHERE entity_type='contact'"
            )
            orgs = self.query_one(
                "SELECT COUNT(*) FROM entity_registry WHERE entity_type='organization'"
            )
            engagements = self.query_one(
                "SELECT COUNT(*) FROM entity_registry WHERE entity_type='engagement'"
            )
            users = self.query_one(
                "SELECT COUNT(*) FROM entity_registry WHERE entity_type='user'"
            )

            projects_ok = projects and projects[0] >= 11
            contacts_ok = contacts and contacts[0] >= 5
            orgs_ok = orgs and orgs[0] >= 2
            engagements_ok = engagements and engagements[0] >= 3
            users_ok = users and users[0] >= 3

            msg = f"Projects:{projects[0] if projects else 0} Contacts:{contacts[0] if contacts else 0} Orgs:{orgs[0] if orgs else 0}"
            self.test_result(
                "test_all_entities_registered",
                projects_ok and contacts_ok and orgs_ok and engagements_ok and users_ok,
                msg
            )
        except Exception as e:
            self.test_result("test_all_entities_registered", False, str(e))

    def test_canonical_identifiers_unique(self):
        """Verify canonical_identifier is unique per entity"""
        try:
            duplicates = self.query("""
                SELECT canonical_identifier, COUNT(*) as cnt
                FROM entity_registry
                GROUP BY canonical_identifier
                HAVING COUNT(*) > 1
            """)
            passed = len(duplicates) == 0
            msg = f"{len(duplicates)} duplicate canonical_ids" if duplicates else "All unique"
            self.test_result("test_canonical_identifiers_unique", passed, msg)
        except Exception as e:
            self.test_result("test_canonical_identifiers_unique", False, str(e))

    def test_authority_tiers_valid(self):
        """Verify authority_tier values are valid"""
        try:
            invalid = self.query_one("""
                SELECT COUNT(*) FROM entity_registry
                WHERE authority_tier NOT IN ('admiral', 'owner', 'member', 'observer')
                AND authority_tier IS NOT NULL
            """)
            passed = invalid and invalid[0] == 0
            msg = f"{invalid[0] if invalid else 0} invalid tiers" if invalid and invalid[0] > 0 else "All valid"
            self.test_result("test_authority_tiers_valid", passed, msg)
        except Exception as e:
            self.test_result("test_authority_tiers_valid", False, str(e))

    def test_source_of_truth_populated(self):
        """Verify source_of_truth field is populated"""
        try:
            null_source = self.query_one("""
                SELECT COUNT(*) FROM entity_registry
                WHERE source_of_truth IS NULL
            """)
            passed = null_source and null_source[0] == 0
            msg = f"{null_source[0] if null_source else 0} null sources"
            self.test_result("test_source_of_truth_populated", passed, msg)
        except Exception as e:
            self.test_result("test_source_of_truth_populated", False, str(e))

    # ============================================================================
    # Relationship Verification Tests (5 tests)
    # ============================================================================

    def test_all_relationships_exist(self):
        """Verify relationships are established"""
        try:
            total = self.query_one("SELECT COUNT(*) FROM entity_memberships")
            count = total[0] if total else 0
            passed = count >= 51
            msg = f"{count} relationships (expected ≥51)"
            self.test_result("test_all_relationships_exist", passed, msg)
        except Exception as e:
            self.test_result("test_all_relationships_exist", False, str(e))

    def test_no_orphaned_relationships(self):
        """Verify all relationship targets exist"""
        try:
            orphaned = self.query("""
                SELECT COUNT(*) FROM entity_memberships em
                LEFT JOIN entity_registry er ON em.target_entity_id = er.entity_id
                WHERE er.entity_id IS NULL
            """)
            count = orphaned[0][0] if orphaned else 0
            passed = count == 0
            msg = f"{count} orphaned relationships" if count > 0 else "No orphans"
            self.test_result("test_no_orphaned_relationships", passed, msg)
        except Exception as e:
            self.test_result("test_no_orphaned_relationships", False, str(e))

    def test_relationship_types_valid(self):
        """Verify relationship_type values are valid"""
        try:
            invalid = self.query_one("""
                SELECT COUNT(*) FROM entity_memberships
                WHERE relationship_type NOT IN ('member-of', 'owns', 'serves', 'uses', 'contributor_to')
            """)
            passed = invalid and invalid[0] == 0
            msg = f"{invalid[0] if invalid else 0} invalid types"
            self.test_result("test_relationship_types_valid", passed, msg)
        except Exception as e:
            self.test_result("test_relationship_types_valid", False, str(e))

    def test_member_of_edges(self):
        """Verify member-of relationships: projects → organizations"""
        try:
            edges = self.query_one("""
                SELECT COUNT(*) FROM entity_memberships
                WHERE relationship_type='member-of'
            """)
            count = edges[0] if edges else 0
            passed = count >= 11
            msg = f"{count} member-of edges (expected ≥11)"
            self.test_result("test_member_of_edges", passed, msg)
        except Exception as e:
            self.test_result("test_member_of_edges", False, str(e))

    def test_contributor_to_edges(self):
        """Verify contributor_to relationships: users → projects"""
        try:
            edges = self.query_one("""
                SELECT COUNT(*) FROM entity_memberships
                WHERE relationship_type='contributor_to'
            """)
            count = edges[0] if edges else 0
            passed = count >= 15
            msg = f"{count} contributor_to edges (expected ≥15)"
            self.test_result("test_contributor_to_edges", passed, msg)
        except Exception as e:
            self.test_result("test_contributor_to_edges", False, str(e))

    # ============================================================================
    # Cross-Practice Integration Tests (4 tests)
    # ============================================================================

    def test_project_discovery_across_practices(self):
        """Verify projects from all practices are registered"""
        try:
            practices_dir = Path("/Users/andersonfamily/practices")
            if not practices_dir.exists():
                self.test_result("test_project_discovery_across_practices", False, "Practices directory not found")
                return

            practices = set()
            for yaml_file in practices_dir.glob("**/.empirica/project.yaml"):
                practice_name = yaml_file.parent.parent.name
                if practice_name and not practice_name.startswith('.'):
                    practices.add(practice_name)

            if not practices:
                self.test_result("test_project_discovery_across_practices", False, "No practices found")
                return

            # Verify at least one project per practice
            found_all = True
            for practice in practices:
                projects = self.query(f"""
                    SELECT COUNT(*) FROM entity_registry
                    WHERE entity_type='project' AND display_name LIKE '%{practice}%'
                """)
                count = projects[0][0] if projects else 0
                if count == 0:
                    found_all = False
                    break

            msg = f"Verified {len(practices)} practices"
            self.test_result("test_project_discovery_across_practices", found_all, msg)
        except Exception as e:
            self.test_result("test_project_discovery_across_practices", False, str(e))

    def test_contact_authority_tiers(self):
        """Verify contacts have correct authority tiers"""
        try:
            # Carly should be admiral
            carly = self.query("""
                SELECT authority_tier FROM entity_registry
                WHERE entity_type='contact'
                AND (canonical_identifier='carly.r.anderson@gmail.com'
                     OR canonical_identifier LIKE '%Carly%')
            """)

            admiral_ok = carly and len(carly) > 0 and carly[0][0] == 'admiral'

            # Other contacts should exist
            others = self.query_one("""
                SELECT COUNT(*) FROM entity_registry
                WHERE entity_type='contact'
                AND authority_tier IN ('member', 'owner', 'observer')
            """)
            others_ok = others and others[0] > 0

            msg = f"Carly tier: {'admiral' if admiral_ok else 'not-admiral'}, others exist: {others_ok}"
            self.test_result("test_contact_authority_tiers", admiral_ok and others_ok, msg)
        except Exception as e:
            self.test_result("test_contact_authority_tiers", False, str(e))

    def test_engagement_project_mapping(self):
        """Verify engagements are linked to projects"""
        try:
            engagements = self.query("""
                SELECT DISTINCT target_entity_id FROM entity_memberships
                WHERE relationship_type='serves' AND target_entity_type='engagement'
            """)
            count = len(engagements)
            passed = count >= 3
            msg = f"{count} engagements (expected ≥3)"
            self.test_result("test_engagement_project_mapping", passed, msg)
        except Exception as e:
            self.test_result("test_engagement_project_mapping", False, str(e))

    def test_registry_graph_consistency(self):
        """Verify registry forms a consistent acyclic graph"""
        try:
            # Check for cycles in uses relationships
            cycles = self.query("""
                WITH RECURSIVE uses_graph AS (
                    SELECT source_entity_id, target_entity_id FROM entity_memberships
                    WHERE relationship_type='uses'
                    UNION ALL
                    SELECT g.source_entity_id, m.target_entity_id
                    FROM uses_graph g
                    JOIN entity_memberships m ON g.target_entity_id = m.source_entity_id
                    WHERE m.relationship_type='uses'
                    LIMIT 1000
                )
                SELECT COUNT(*) FROM uses_graph
                WHERE source_entity_id = target_entity_id
            """)
            count = cycles[0][0] if cycles else 0
            passed = count == 0
            msg = f"{count} cycles found" if count > 0 else "No cycles"
            self.test_result("test_registry_graph_consistency", passed, msg)
        except Exception as e:
            self.test_result("test_registry_graph_consistency", False, str(e))

    # ============================================================================
    # Performance Test
    # ============================================================================

    def test_query_performance(self):
        """Verify registry queries complete within SLA (100ms)"""
        try:
            test_queries = [
                ("Find projects in organization", """
                    SELECT p.display_name FROM entity_registry p
                    JOIN entity_memberships em ON p.entity_id = em.source_entity_id
                    WHERE em.relationship_type='member-of'
                    LIMIT 20
                """),
                ("Find contacts and project counts", """
                    SELECT c.display_name, COUNT(p.entity_id)
                    FROM entity_registry c
                    LEFT JOIN entity_memberships em ON c.entity_id = em.source_entity_id
                    WHERE c.entity_type='contact' OR em.relationship_type='owns'
                    GROUP BY c.entity_id
                    LIMIT 20
                """),
                ("Find serving relationships", """
                    SELECT p.display_name FROM entity_registry p
                    JOIN entity_memberships em ON p.entity_id = em.source_entity_id
                    WHERE em.relationship_type='serves'
                    LIMIT 20
                """),
            ]

            all_passed = True
            for query_name, query_sql in test_queries:
                start = time.time()
                self.query(query_sql)
                elapsed = (time.time() - start) * 1000  # Convert to ms
                passed = elapsed < 100
                all_passed = all_passed and passed
                msg = f"{elapsed:.1f}ms"
                self.test_result(f"query_perf: {query_name}", passed, msg)
        except Exception as e:
            self.test_result("test_query_performance", False, str(e))

    # ============================================================================
    # Sync Pipeline Test
    # ============================================================================

    def test_sync_pipeline_no_duplicates(self):
        """Verify sync pipeline doesn't create duplicates"""
        try:
            duplicates = self.query("""
                SELECT canonical_identifier, COUNT(*)
                FROM entity_registry
                GROUP BY canonical_identifier
                HAVING COUNT(*) > 1
            """)
            passed = len(duplicates) == 0
            msg = f"{len(duplicates)} duplicate canonical_ids" if duplicates else "No duplicates"
            self.test_result("test_sync_pipeline_no_duplicates", passed, msg)
        except Exception as e:
            self.test_result("test_sync_pipeline_no_duplicates", False, str(e))

    # ============================================================================
    # Main execution
    # ============================================================================

    def run_all_tests(self):
        """Run complete verification suite"""
        print("\nM2 Rank 3: Registry Verification Suite")
        print("=" * 70)

        print("\n[Entity Verification Tests]")
        self.test_all_entities_registered()
        self.test_canonical_identifiers_unique()
        self.test_authority_tiers_valid()
        self.test_source_of_truth_populated()

        print("\n[Relationship Verification Tests]")
        self.test_all_relationships_exist()
        self.test_no_orphaned_relationships()
        self.test_relationship_types_valid()
        self.test_member_of_edges()
        self.test_contributor_to_edges()

        print("\n[Cross-Practice Integration Tests]")
        self.test_project_discovery_across_practices()
        self.test_contact_authority_tiers()
        self.test_engagement_project_mapping()
        self.test_registry_graph_consistency()

        print("\n[Performance Tests]")
        self.test_query_performance()

        print("\n[Sync Pipeline Tests]")
        self.test_sync_pipeline_no_duplicates()

        print()
        self.print_summary()

    def print_summary(self):
        """Print test results summary"""
        passed = sum(1 for r in self.test_results if r['status'] == 'PASS')
        failed = sum(1 for r in self.test_results if r['status'] == 'FAIL')
        total = len(self.test_results)

        print("Test Results Summary:")
        print("-" * 70)
        print(f"Passed: {passed}/{total}")
        print(f"Failed: {failed}/{total}")

        if failed > 0:
            print("\nFailed tests:")
            for test in self.test_results:
                if test['status'] == 'FAIL':
                    print(f"  ✗ {test['name']}: {test['message']}")

        print()
        if failed == 0:
            print("✓ All tests passed — Ready for production")
            return True
        else:
            print("✗ Some tests failed — Review errors before production")
            return False

    def close(self):
        """Close database connection"""
        if self.db:
            self.db.close()


if __name__ == "__main__":
    suite = RegistryVerificationSuite()
    try:
        suite.run_all_tests()
    finally:
        suite.close()
