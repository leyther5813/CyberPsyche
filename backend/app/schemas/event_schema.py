
from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class BehaviourEventDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scenario_id: str = Field(min_length=1)
    event_type: Literal[
        "view",
        "open_evidence",
        "action",
        "reason",
        "confidence",
    ]
    payload: Optional[Dict[str, Any]] = None
    ts: Optional[str] = None

    @field_validator("scenario_id")
    @classmethod
    def validate_scenario_id(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("scenario_id must not be empty")

        return value

    @field_validator("payload")
    @classmethod
    def validate_payload(cls, payload, info):
        if info.data.get("event_type") == "open_evidence":
            evidence_id = payload.get("evidence_id") if payload else None

            if not isinstance(evidence_id, str) or not evidence_id.strip():
                raise ValueError(
                    "open_evidence requires a non-empty string evidence_id"
                )

        return payload
