from __future__ import annotations

import datetime
import json
import uuid
from typing import Any, Dict, List
from .models import ComponentType, SystemManifest


def to_cyclonedx_type(c_type: ComponentType) -> str:
    """Map internal AI component type to standard CycloneDX 1.6 component type."""
    mapping = {
        ComponentType.MODEL: "machine-learning-model",
        ComponentType.VECTOR_DB: "data",
        ComponentType.GUARDRAIL: "library",
        ComponentType.FRAMEWORK: "framework",
        ComponentType.DATA_SOURCE: "data",
    }
    return mapping.get(c_type, "library")


def sanitize_purl_name(name: str) -> str:
    """Sanitize human readable name for Package URL format."""
    clean = name.lower().replace(" ", "-").replace("_", "-")
    return "".join(c for c in clean if c.isalnum() or c in ("-", "."))


def generate_cyclonedx_bom(manifest: SystemManifest) -> Dict[str, Any]:
    """Generate a CycloneDX 1.6 compliant AI Software Bill of Materials (AI-BOM) dict."""
    timestamp = manifest.timestamp or datetime.datetime.now(datetime.timezone.utc).isoformat()
    bom_uuid = f"urn:uuid:{uuid.uuid4()}"

    components_payload: List[Dict[str, Any]] = []
    for c in manifest.components:
        cdx_type = to_cyclonedx_type(c.component_type)
        purl_name = sanitize_purl_name(c.name)
        ver = c.version_or_variant if c.version_or_variant != "unknown" else "0.0.0"

        comp_dict: Dict[str, Any] = {
            "type": cdx_type,
            "name": c.name,
            "version": c.version_or_variant,
            "purl": f"pkg:generic/{purl_name}@{ver}",
            "evidence": {
                "occurrences": [
                    {
                        "location": c.file_path,
                    }
                ]
            },
            "properties": [
                {
                    "name": "ai:governance:componentType",
                    "value": c.component_type.value,
                },
                {
                    "name": "ai:governance:detectedSignature",
                    "value": c.evidence,
                },
                {
                    "name": "ai:governance:lineageFile",
                    "value": c.file_path,
                },
            ],
        }

        # If it's a machine learning model, include specialized CycloneDX model metadata
        if c.component_type == ComponentType.MODEL:
            comp_dict["modelCard"] = {
                "modelParameters": {
                    "task": "Generative Language & Reasoning",
                    "architectureFamily": c.name,
                },
                "properties": [
                    {
                        "name": "ai:safety:auditReadiness",
                        "value": "governance-verified",
                    }
                ],
            }

        components_payload.append(comp_dict)

    return {
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "serialNumber": bom_uuid,
        "version": 1,
        "metadata": {
            "timestamp": timestamp,
            "tools": {
                "components": [
                    {
                        "type": "application",
                        "author": "Ashish Dhillon",
                        "name": "ai-manifest",
                        "version": "0.2.0",
                        "description": "Automated component inventory and system card generator for AI applications",
                    }
                ]
            },
            "component": {
                "type": "application",
                "name": manifest.project_name,
                "description": f"AI Application architecture and component manifest for {manifest.project_name}",
            },
        },
        "components": components_payload,
    }


def format_cyclonedx_json(manifest: SystemManifest) -> str:
    """Format manifest as indented CycloneDX 1.6 JSON string."""
    bom = generate_cyclonedx_bom(manifest)
    return json.dumps(bom, indent=2)
