from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any
from datetime import datetime

VALID_ACTIONS = {
    "PROCEED", "IGNORE", "REPLY_TO_SENDER", "VERIFY_INDEPENDENTLY",
    "REPORT", "ASK_TRUSTED_PERSON", "GATHER_MORE_EVIDENCE", "UNSURE"
}

class DecisionSubmissionDTO(BaseModel):
    scenario_id: str
    action: str  # PROCEED | IGNORE | REPLY_TO_SENDER | VERIFY_INDEPENDENTLY | REPORT | ASK_TRUSTED_PERSON | GATHER_MORE_EVIDENCE | UNSURE
    reason_tags: List[str]
    free_text: Optional[str] = None
    confidence: int = Field(..., ge=1, le=5)
    latency_ms: int = Field(..., ge=0)

    @field_validator("action", mode="before")
    @classmethod
    def validate_and_normalize_action(cls, v: Any) -> str:
        if not isinstance(v, str):
            raise ValueError("Action must be a string")
        norm = v.strip().upper()
        if norm not in VALID_ACTIONS:
            raise ValueError(f"Invalid action '{v}'. Allowed actions are: {sorted(list(VALID_ACTIONS))}")
        return norm

class DecisionOutcomeResponseDTO(BaseModel):
    decision_id: str
    status: str = "recorded"
    # Note: Ground truth and decision quality are NOT returned during baseline/retest!

