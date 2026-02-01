"""
IBM TrustBuild — Governance Policy Knowledge Base
The structured rulebook that the Auditor Agent enforces.
Each policy has detection logic and an auto-correction strategy.
"""

from typing import List, Callable
from dataclasses import dataclass, field


@dataclass
class GovernancePolicy:
    """A single compliance rule in the knowledge base."""
    policy_id: str
    policy_name: str
    framework: str                  # HIPAA, SOC2, GDPR, IBM_BASELINE
    severity: str                   # critical, warning, info
    description: str
    check_fn: Callable              # Function: (manifest dict) -> bool (True = PASS)
    correction_fn: Callable         # Function: (manifest dict) -> manifest dict (auto-fix)
    correction_description: str     # Human-readable explanation of the fix


# ─────────────────────────────────────────────
# Policy Check Functions
# ─────────────────────────────────────────────

def check_vpc_isolation(manifest: dict) -> bool:
    """FAIL if data sensitivity is PHI/PII but VPC is not enabled."""
    sensitivity = manifest.get("detected_sensitivity", "public")
    networking = manifest.get("networking", {})
    if sensitivity in ("PHI", "PII") and not networking.get("vpc_enabled", False):
        return False
    return True


def check_encryption_at_rest(manifest: dict) -> bool:
    """FAIL if any database service lacks encryption at rest."""
    security = manifest.get("security_config", {})
    services = manifest.get("services", [])
    has_db = any(s.get("role") == "database" for s in services)
    if has_db and not security.get("encryption_at_rest", False):
        return False
    return True


def check_encryption_in_transit(manifest: dict) -> bool:
    """FAIL if TLS/encryption in transit is not enabled."""
    security = manifest.get("security_config", {})
    if not security.get("encryption_in_transit", False):
        return False
    return True


def check_audit_logging_for_phi(manifest: dict) -> bool:
    """FAIL if PHI data is processed but audit logging is off."""
    sensitivity = manifest.get("detected_sensitivity", "public")
    security = manifest.get("security_config", {})
    if sensitivity == "PHI" and not security.get("audit_logging", False):
        return False
    return True


def check_private_endpoints(manifest: dict) -> bool:
    """FAIL if PHI/PCI data uses public endpoints."""
    sensitivity = manifest.get("detected_sensitivity", "public")
    networking = manifest.get("networking", {})
    if sensitivity in ("PHI", "PCI") and not networking.get("private_endpoints", False):
        return False
    return True


def check_no_public_api_for_sensitive_data(manifest: dict) -> bool:
    """FAIL if sensitive data services are exposed without VPC."""
    sensitivity = manifest.get("detected_sensitivity", "public")
    networking = manifest.get("networking", {})
    if sensitivity in ("PHI", "PII", "PCI"):
        if not networking.get("vpc_enabled", False):
            return False
        if not networking.get("subnet_isolation", False):
            return False
    return True


def check_iam_policies_present(manifest: dict) -> bool:
    """FAIL if IAM policies are missing for enterprise workloads."""
    sensitivity = manifest.get("detected_sensitivity", "public")
    security = manifest.get("security_config", {})
    if sensitivity in ("PHI", "PCI") and not security.get("iam_policies", False):
        return False
    return True


def check_region_compliance(manifest: dict) -> bool:
    """FAIL if GDPR-applicable data is stored outside EU regions."""
    frameworks = manifest.get("applicable_frameworks", [])
    services = manifest.get("services", [])
    if "GDPR" in frameworks:
        for svc in services:
            if svc.get("role") == "database" and svc.get("region", "") not in ("eu-gb", "eu-de", "eu-fr"):
                return False
    return True


# ─────────────────────────────────────────────
# Auto-Correction Functions
# ─────────────────────────────────────────────

def correct_vpc_isolation(manifest: dict) -> dict:
    manifest.setdefault("networking", {})
    manifest["networking"]["vpc_enabled"] = True
    manifest["networking"]["subnet_isolation"] = True
    manifest["networking"]["private_endpoints"] = True
    return manifest


def correct_encryption_at_rest(manifest: dict) -> dict:
    manifest.setdefault("security_config", {})
    manifest["security_config"]["encryption_at_rest"] = True
    # Upgrade database plans to dedicated if PHI
    if manifest.get("detected_sensitivity") == "PHI":
        for svc in manifest.get("services", []):
            if svc.get("role") == "database":
                svc["plan"] = "dedicated"
    return manifest


def correct_encryption_in_transit(manifest: dict) -> dict:
    manifest.setdefault("security_config", {})
    manifest["security_config"]["encryption_in_transit"] = True
    return manifest


def correct_audit_logging(manifest: dict) -> dict:
    manifest.setdefault("security_config", {})
    manifest["security_config"]["audit_logging"] = True
    return manifest


def correct_private_endpoints(manifest: dict) -> dict:
    manifest.setdefault("networking", {})
    manifest["networking"]["private_endpoints"] = True
    return manifest


def correct_public_api_exposure(manifest: dict) -> dict:
    manifest.setdefault("networking", {})
    manifest["networking"]["vpc_enabled"] = True
    manifest["networking"]["subnet_isolation"] = True
    manifest["networking"]["private_endpoints"] = True
    return manifest


def correct_iam_policies(manifest: dict) -> dict:
    manifest.setdefault("security_config", {})
    manifest["security_config"]["iam_policies"] = True
    return manifest


def correct_region_gdpr(manifest: dict) -> dict:
    for svc in manifest.get("services", []):
        if svc.get("role") == "database":
            svc["region"] = "eu-gb"
    return manifest


# ─────────────────────────────────────────────
# The Policy Knowledge Base Registry
# ─────────────────────────────────────────────

POLICY_KNOWLEDGE_BASE: List[GovernancePolicy] = [
    GovernancePolicy(
        policy_id="POL-HIPAA-001",
        policy_name="Database VPC Isolation Required",
        framework="HIPAA",
        severity="critical",
        description="All PHI data stores must be isolated within a Virtual Private Cloud with private endpoints only. Public access is strictly prohibited.",
        check_fn=check_vpc_isolation,
        correction_fn=correct_vpc_isolation,
        correction_description="Enabled VPC isolation and configured private endpoints for all database services."
    ),
    GovernancePolicy(
        policy_id="POL-HIPAA-002",
        policy_name="Encryption at Rest Required for PHI",
        framework="HIPAA",
        severity="critical",
        description="All Protected Health Information must be encrypted at rest using AES-256 or equivalent. Database plan must be 'dedicated' tier minimum.",
        check_fn=check_encryption_at_rest,
        correction_fn=correct_encryption_at_rest,
        correction_description="Enabled encryption at rest and upgraded database to dedicated tier for PHI compliance."
    ),
    GovernancePolicy(
        policy_id="POL-HIPAA-003",
        policy_name="Audit Logging Required for PHI Access",
        framework="HIPAA",
        severity="critical",
        description="All access to PHI must be logged for audit trail compliance. Logging must be enabled at the infrastructure level.",
        check_fn=check_audit_logging_for_phi,
        correction_fn=correct_audit_logging,
        correction_description="Enabled infrastructure-level audit logging for all PHI access points."
    ),
    GovernancePolicy(
        policy_id="POL-IBM-001",
        policy_name="Encryption in Transit Required",
        framework="IBM_BASELINE",
        severity="critical",
        description="All data in transit between services must be encrypted using TLS 1.2 or higher. This is a baseline requirement for all IBM Cloud deployments.",
        check_fn=check_encryption_in_transit,
        correction_fn=correct_encryption_in_transit,
        correction_description="Enabled TLS encryption for all service-to-service communication."
    ),
    GovernancePolicy(
        policy_id="POL-IBM-002",
        policy_name="Private Endpoints for Sensitive Data",
        framework="IBM_BASELINE",
        severity="warning",
        description="Services handling sensitive data (PHI, PCI, PII) should use private endpoints to avoid routing traffic over the public internet.",
        check_fn=check_private_endpoints,
        correction_fn=correct_private_endpoints,
        correction_description="Configured private endpoints for all sensitive data services."
    ),
    GovernancePolicy(
        policy_id="POL-SEC-001",
        policy_name="No Public API Exposure for Sensitive Data",
        framework="IBM_BASELINE",
        severity="critical",
        description="Services processing PHI, PII, or PCI data must not be publicly accessible. VPC and subnet isolation are mandatory.",
        check_fn=check_no_public_api_for_sensitive_data,
        correction_fn=correct_public_api_exposure,
        correction_description="Enabled VPC isolation and subnet segregation to prevent public API exposure."
    ),
    GovernancePolicy(
        policy_id="POL-SEC-002",
        policy_name="IAM Policies Required for Enterprise Workloads",
        framework="IBM_BASELINE",
        severity="warning",
        description="Enterprise workloads handling regulated data must have explicit IAM policies defined for role-based access control.",
        check_fn=check_iam_policies_present,
        correction_fn=correct_iam_policies,
        correction_description="Added IAM role-based access control policies for all regulated data services."
    ),
    GovernancePolicy(
        policy_id="POL-GDPR-001",
        policy_name="EU Data Residency for GDPR",
        framework="GDPR",
        severity="critical",
        description="Data subject to GDPR must be stored and processed within EU regions only. Acceptable regions: eu-gb, eu-de, eu-fr.",
        check_fn=check_region_compliance,
        correction_fn=correct_region_gdpr,
        correction_description="Migrated all database services to EU region (eu-gb) for GDPR compliance."
    ),
]


def get_policies_for_frameworks(frameworks: List[str]) -> List[GovernancePolicy]:
    """
    Filter the knowledge base to only return policies relevant
    to the detected compliance frameworks.
    Always includes IBM_BASELINE policies.
    """
    relevant = []
    frameworks_set = set(frameworks)
    frameworks_set.add("IBM_BASELINE")  # Always enforce baseline

    for policy in POLICY_KNOWLEDGE_BASE:
        if policy.framework in frameworks_set:
            relevant.append(policy)
    return relevant
