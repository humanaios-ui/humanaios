"""Synthetic reviewer badge lifecycle checks; not for production issuance."""

import hashlib
import hmac
import json
from typing import Any, Dict, Set


VC_CONTEXT = "https://www.w3.org/ns/credentials/v2"
OPEN_BADGES_CONTEXT = "https://purl.imsglobal.org/spec/ob/v3p0/context.json"
SYNTHETIC_PROOF_TYPE = "SyntheticHmacSha256Proof"


def _canonical_bytes(credential: Dict[str, Any]) -> bytes:
    payload = dict(credential)
    proof = payload.get("proof")
    if isinstance(proof, dict):
        proof = dict(proof)
        proof.pop("proofValue", None)
        payload["proof"] = proof
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


class SyntheticCredentialIssuer:
    """Issue test credentials and model issuer-side revocation."""

    def __init__(self, issuer: str, signing_key: bytes):
        if not isinstance(issuer, str) or not issuer.strip():
            raise ValueError("issuer must be a non-empty string")
        if not isinstance(signing_key, bytes) or len(signing_key) < 32:
            raise ValueError("signing_key must contain at least 32 bytes")
        self.issuer = issuer
        self._signing_key = signing_key
        self._revoked: Set[str] = set()
        self._next_status_index = 0

    def issue(
        self,
        credential_id: str,
        subject_id: str,
        achievement_id: str,
        achievement_name: str,
        issued_at: str,
    ) -> Dict[str, Any]:
        values = {
            "credential_id": credential_id,
            "subject_id": subject_id,
            "achievement_id": achievement_id,
            "achievement_name": achievement_name,
            "issued_at": issued_at,
        }
        if any(
            not isinstance(value, str) or not value.strip()
            for value in values.values()
        ):
            raise ValueError("credential fields must be non-empty strings")

        self._next_status_index += 1
        credential = {
            "@context": [VC_CONTEXT, OPEN_BADGES_CONTEXT],
            "id": credential_id,
            "type": ["VerifiableCredential", "OpenBadgeCredential"],
            "issuer": self.issuer,
            "validFrom": issued_at,
            "credentialSubject": {
                "id": subject_id,
                "type": "AchievementSubject",
                "achievement": {
                    "id": achievement_id,
                    "type": "Achievement",
                    "name": achievement_name,
                },
            },
            "credentialStatus": {
                "id": f"{credential_id}#status",
                "type": "BitstringStatusListEntry",
                "statusPurpose": "revocation",
                "statusListIndex": str(self._next_status_index - 1),
                "statusListCredential": (
                    f"{self.issuer.rstrip('/')}/credential-status-list/1"
                ),
            },
        }
        credential["proof"] = {
            "type": SYNTHETIC_PROOF_TYPE,
            "proofPurpose": "assertionMethod",
            "verificationMethod": f"{self.issuer}#synthetic-key",
            "created": issued_at,
        }
        credential["proof"]["proofValue"] = hmac.new(
            self._signing_key, _canonical_bytes(credential), hashlib.sha256
        ).hexdigest()
        return credential

    def revoke(self, credential_id: str) -> None:
        if not isinstance(credential_id, str) or not credential_id.strip():
            raise ValueError("credential_id must be a non-empty string")
        self._revoked.add(credential_id)

    def verify(self, credential: Any) -> bool:
        if not isinstance(credential, dict):
            return False
        proof = credential.get("proof")
        if (
            credential.get("issuer") != self.issuer
            or not isinstance(credential.get("id"), str)
            or credential.get("id") in self._revoked
            or not isinstance(proof, dict)
            or proof.get("type") != SYNTHETIC_PROOF_TYPE
            or proof.get("verificationMethod") != f"{self.issuer}#synthetic-key"
            or not isinstance(proof.get("proofValue"), str)
        ):
            return False
        try:
            expected = hmac.new(
                self._signing_key, _canonical_bytes(credential), hashlib.sha256
            ).hexdigest()
        except (TypeError, ValueError, RecursionError):
            return False
        return hmac.compare_digest(proof["proofValue"], expected)
