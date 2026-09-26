"""
M2 Rank 3 Phase 6: Registry Verification & Testing
Uses workspace database (~/.empirica/workspace/workspace.db)
"""

import sqlite3
from pathlib import Path

class RegistryVerificationSuite:
    def __init__(self, db_path: str = None):
        if db_path is None:
            home = Path.home()
            db_path = str(home / ".empirica" / "workspace" / "workspace.db")
        
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
        print("\nM2 Rank 3: Registry Verification Suite")
        print("=" * 70)

        print("\n[Entity Verification Tests]")
        try:
            projects = self.query_one("SELECT COUNT(*) FROM entity_registry WHERE entity_type='project'")
            contacts = self.query_one("SELECT COUNT(*) FROM entity_registry WHERE entity_type='contact'")
            orgs = self.query_one("SELECT COUNT(*) FROM entity_registry WHERE entity_type='organization'")
            engagements = self.query_one("SELECT COUNT(*) FROM entity_registry WHERE entity_type='engagement'")
            
            projects_ok = projects and projects[0] > 0
            msg = f"Projects:{projects[0] if projects else 0} Contacts:{contacts[0] if contacts else 0} Orgs:{orgs[0] if orgs else 0}"
            self.test_result("test_entities_exist", projects_ok, msg)
        except Exception as e:
            self.test_result("test_entities_exist", False, str(e))

        print("\n[Relationship Verification Tests]")
        try:
            total = self.query_one("SELECT COUNT(*) FROM entity_memberships")
            count = total[0] if total else 0
            passed = count > 0
            msg = f"{count} relationships"
            self.test_result("test_relationships_exist", passed, msg)
        except Exception as e:
            self.test_result("test_relationships_exist", False, str(e))

        print("\n[Entity Registry Status]")
        try:
            # Show summary
            for entity_type in ['project', 'contact', 'organization', 'engagement', 'user']:
                count = self.query_one(f"SELECT COUNT(*) FROM entity_registry WHERE entity_type=?", (entity_type,))
                if count:
                    print(f"  {entity_type.capitalize():15} : {count[0]:3} entities")
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
            print("\n✓ Entity registry is POPULATED and ready for Phase 6")
            return True
        else:
            print("\n✗ Some tests failed")
            return False

if __name__ == "__main__":
    suite = RegistryVerificationSuite()
    try:
        suite.run_all_tests()
    finally:
        suite.db.close()
