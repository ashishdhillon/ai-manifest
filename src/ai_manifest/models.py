from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class ComponentType(str, Enum):
    MODEL = "model"
    VECTOR_DB = "vector_db"
    GUARDRAIL = "guardrail"
    DATA_SOURCE = "data_source"
    FRAMEWORK = "framework"


@dataclass(frozen=True)
class AIComponent:
    name: str
    component_type: ComponentType
    evidence: str
    file_path: str
    version_or_variant: str = "unknown"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "component_type": self.component_type.value,
            "evidence": self.evidence,
            "file_path": self.file_path,
            "version_or_variant": self.version_or_variant,
        }


@dataclass
class SystemManifest:
    project_name: str
    components: List[AIComponent] = field(default_factory=list)
    timestamp: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_name": self.project_name,
            "timestamp": self.timestamp or datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "component_count": len(self.components),
            "components": [c.to_dict() for c in self.components],
        }
