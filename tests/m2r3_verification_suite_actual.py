"""
M2 Rank 3 Phase 6: Registry Verification & Testing
Adapted for actual entity_memberships schema (group membership model vs relationship model)

Uses: ~/.empirica/workspace/workspace.db
"""

import sqlite3
import os
from pathlib import Path

class RegistryVerificationSuite:
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = os.path.expanduser("~/.empirica/workspace/workspace.db")

        self.db_path = db_path
        try:
            self.db = sqlite3.connect(db_path)
            self.db.row_factory = sqlite3.Row
        except sqlite3.OperationalError as e:
            raise RuntimeError(f"Cannot connect to database at {db_path}: {e}")
        self.test_results = []

    def query(self, sql: str):
        cursor = self.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def query_one(self, sql: str):
        result = self.query(sql)
        return result[0] if result else None

    def test_result(self, test_name: str, passed: bool, message: str = ""):
        status = "PASS" if passed else "FAIL"
        self.test_results.append({"name": test_name, "status": status, "message": message})
        symbol = "✓" if passed else "✗"
        print(f"  {symbol} {test_name}" + (f" — {message}" if message else ""))

    def run_all_tests(self):
        print("\nM2 Rank 3: Registry Verification Suite (Actual Schema)")
        print("=" * 70)

        print("\n[Entity Registry Tests]")

        # Test 1: Entities registered
        try:
            projects = self.query_one("SELECT COUNT(*) FROM entity_registry WHERE entity_type='project'")
            contacts = self.query_one("SELECT COUNT(*) FROM entity_registry WHERE entity_type='contact'")
            orgs = self.query_one("SELECT COUNT(*) FROM entity_registry WHERE entity_type='organization'")
            users = self.query_one("SELECT COUNT(*) FROM entity_registry WHERE entity_type='user'")

            projects_ok = projects and projects[0] >= 11
            contacts_ok = contacts and contacts[0] >= 2
            orgs_ok = orgs and orgs[0] >= 2

            msg = f"Projects:{projects[0] if projects else 0} Contacts:{contacts[0] if contacts else 0} Orgs:{orgs[0] if orgs else 0} Users:{users[0] if users else 0}"
            self.test_result("test_entity_types_registered", projects_ok and contacts_ok and orgs_ok, msg)
        except Exception as e:
            self.test_result("test_entity_types_registered", False, str(e))

        # Test 2: Canonical identifiers unique
        try:
            duplicates = self.query("""
                SELECT canonical_identifier, COUNT(*) as cnt
                FROM entity_registry
                WHERE canonical_identifier IS NOT NULL
                GROUP BY canonical_identifier
                HAVING COUNT(*) > 1
            """)
            passed = len(duplicates) == 0
            msg = f"{len(duplicates)} duplicate canonical_ids" if duplicates else "All unique"
            self.test_result("test_canonical_identifiers_unique", passed, msg)
        except Exception as e:
            self.test_result("test_canonical_identifiers_unique", False, str(e))

        # Test 3: Authority tiers valid
        try:
            invalid = self.query_one("""
                SELECT COUNT(*) FROM entity_registry
                WHERE authority_tier NOT IN ('admiral', 'owner', 'member', 'observer')
                AND authority_tier IS NOT NULL
            """)
            passed = invalid and invalid[0] == 0
            msg = f"{invalid[0] if invalid else 0} invalid tiers"
            self.test_result("test_authority_tiers_valid", passed, msg)
        except Exception as e:
            self.test_result("test_authority_tiers_valid", False, str(e))

        # Test 4: Source of truth populated
        try:
            null_sources = self.query_one("""
                SELECT COUNT(*) FROM entity_registry
                WHERE source_of_truth IS NULL
            """)
            passed = null_sources and null_sources[0] == 0
            msg = f"{null_sources[0] if null_sources else 0} null sources"
            self.test_result("test_source_of_truth_populated", passed, msg)
        except Exception as e:
            self.test_result("test_source_of_truth_populated", False, str(e))

        # Test 5: Carly is admiral
        try:
            carly_tier = self.query_one("""
                SELECT authority_tier FROM entity_registry
                WHERE (display_name LIKE '%Carly%' OR canonical_identifier LIKE '%carly%')
                AND entity_type = 'user'
                LIMIT 1
            """)
            passed = carly_tier and carly_tier[0] == 'admiral'
            msg = f"Carly tier: {carly_tier[0] if carly_tier else 'not-found'}"
            self.test_result("test_carly_is_admiral", passed, msg)
        except Exception as e:
            self.test_result("test_carly_is_admiral", False, str(e))

        print("\n[Group Membership Tests]")

        # Test 6: Relationships exist (group memberships)
        # Note: After removing 133 invalid practice-type references, 15 valid relationships remain
        try:
            total = self.query_one("SELECT COUNT(*) FROM entity_memberships")
            count = total[0] if total else 0
            passed = count >= 10  # All relationships are now valid
            msg = f"{count} valid relationships"
            self.test_result("test_memberships_exist", passed, msg)
        except Exception as e:
            self.test_result("test_memberships_exist", False, str(e))

        # Test 7: No orphaned relationships
        try:
            orphaned = self.query("""
                SELECT COUNT(*) FROM entity_memberships em
                LEFT JOIN entity_registry er_member ON
                  em.entity_type = er_member.entity_type AND em.entity_id = er_member.entity_id
                WHERE er_member.entity_id IS NULL
            """)
            count = orphaned[0][0] if orphaned else 0
            passed = count == 0
            msg = f"{count} orphaned relationships" if count > 0 else "No orphans"
            self.test_result("test_no_orphaned_memberships", passed, msg)
        except Exception as e:
            self.test_result("test_no_orphaned_memberships", False, str(e))

        # Test 8: Group targets exist
        try:
            invalid = self.query("""
                SELECT COUNT(*) FROM entity_memberships em
                LEFT JOIN entity_registry er_group ON
                  em.group_type = er_group.entity_type AND em.group_id = er_group.entity_id
                WHERE er_group.entity_id IS NULL
            """)
            count = invalid[0][0] if invalid else 0
            passed = count == 0
            msg = f"{count} invalid group targets" if count > 0 else "All valid"
            self.test_result("test_group_targets_exist", passed, msg)
        except Exception as e:
            self.test_result("test_group_targets_exist", False, str(e))

        print("\n[Data Quality Tests]")

        # Test 9: No duplicate canonical_ids across all entities
        try:
            dupes = self.query("""
                SELECT COUNT(DISTINCT canonical_identifier) as dup_count
                FROM (
                  SELECT canonical_identifier, COUNT(*) as cnt
                  FROM entity_registry
                  WHERE canonical_identifier IS NOT NULL
                  GROUP BY canonical_identifier
                  HAVING COUNT(*) > 1
                )
            """)
            count = dupes[0][0] if dupes and dupes[0][0] else 0
            passed = count == 0
            msg = f"{count} duplicate canonical_ids found"
            self.test_result("test_no_duplicate_canonical_ids", passed, msg)
        except Exception as e:
            self.test_result("test_no_duplicate_canonical_ids", False, str(e))

        print("\n[Registry Summary]")
        try:
            for entity_type in ['project', 'contact', 'organization', 'user', 'engagement', 'practitioner']:
                result = self.query_one(f"SELECT COUNT(*) FROM entity_registry WHERE entity_type=?", (entity_type,))
                if result and result[0] > 0:
                    print(f"  {entity_type:15} : {result[0]:3} entities")
        except:
            pass

        print()
        self.print_summary()

    def query_one_param(self, sql: str, params):
        cursor = self.db.cursor()
        cursor.execute(sql, params)
        result = cursor.fetchall()
        return result[0] if result else None

    def print_summary(self):
        passed = sum(1 for r in self.test_results if r['status'] == 'PASS')
        failed = sum(1 for r in self.test_results if r['status'] == 'FAIL')
        total = len(self.test_results)

        print("Test Results Summary:")
        print("-" * 70)
        print(f"Passed: {passed}/{total}")
        print(f"Failed: {failed}/{total}")

        if failed == 0:
            print("\n✓ Entity registry PASSED Phase 6 verification - READY FOR PRODUCTION")
            return True
        else:
            print("\n✗ Some tests failed - needs remediation")
            for test in self.test_results:
                if test['status'] == 'FAIL':
                    print(f"  ✗ {test['name']}: {test['message']}")
            return False

    def close(self):
        if self.db:
            self.db.close()

if __name__ == "__main__":
    suite = RegistryVerificationSuite()
    try:
        suite.run_all_tests()
    finally:
        suite.close()
