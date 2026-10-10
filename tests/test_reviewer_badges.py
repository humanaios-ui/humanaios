import copy
import unittest

from src.reviewer_badges import SyntheticCredentialIssuer


class TestSyntheticReviewerCredentials(unittest.TestCase):
    def setUp(self):
        self.issuer = SyntheticCredentialIssuer(
            "https://credentials.example/issuers/review", b"x" * 32
        )
        self.credential = self.issuer.issue(
            credential_id="urn:uuid:credential-1",
            subject_id="urn:humanaios:reviewer:pseudonym-1",
            achievement_id="urn:humanaios:achievement:evidence-reviewer",
            achievement_name="Evidence Reviewer",
            issued_at="2026-10-10T00:00:00Z",
        )

    def test_issued_credential_verifies(self):
        self.assertTrue(self.issuer.verify(self.credential))

    def test_revoked_credential_fails_verification(self):
        self.issuer.revoke(self.credential["id"])
        self.assertFalse(self.issuer.verify(self.credential))

    def test_tampered_claim_fails_verification(self):
        tampered = copy.deepcopy(self.credential)
        tampered["credentialSubject"]["achievement"]["name"] = "Assurance Reviewer"
        self.assertFalse(self.issuer.verify(tampered))

    def test_tampered_proof_metadata_fails_verification(self):
        tampered = copy.deepcopy(self.credential)
        tampered["proof"]["proofPurpose"] = "authentication"
        self.assertFalse(self.issuer.verify(tampered))

    def test_rejects_non_credential_and_wrong_issuer(self):
        self.assertFalse(self.issuer.verify(None))
        tampered = copy.deepcopy(self.credential)
        tampered["issuer"] = "https://other.example/issuer"
        self.assertFalse(self.issuer.verify(tampered))


if __name__ == "__main__":
    unittest.main()
