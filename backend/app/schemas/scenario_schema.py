from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class EvidenceItemBase(BaseModel):
    id: str
    label: str
    value: str
    signal: str  # suspicious | neutral | trustworthy | hidden
    diagnosticity: str  # high | medium | low
    official_channel: bool = False

class EvidenceItemScrubbed(BaseModel):
    """Participant-facing evidence DTO without signal/diagnosticity or value before opening."""
    id: str
    label: str

class EvidenceItemRevealed(BaseModel):
    """Returned ONLY after valid OPEN_EVIDENCE event."""
    id: str
    label: str
    value: str

class ScenarioBase(BaseModel):
    scenario_id: str
    family_id: str
    phase_pool: str
    context: str
    channel: str
    persona: str
    truth: str
    mechanisms: List[str]
    pressure: str
    difficulty: str
    narrative: str
    message: Dict[str, Any]
    evidence: List[EvidenceItemBase]
    actions: Dict[str, List[str]]
    consequence_text: Dict[str, str]
    teaching_point: str
    transfer_group: str

class ScrubbedNextScenarioResponse(BaseModel):
    """
    Participant-facing next scenario payload.
    STRICT SECURITY RULE: Ground truth, evidence signals, diagnosticity,
    official channel flags, and action safety classifications ARE SCRUBBED.
    """
    session_id: str
    scenario_id: str
    phase: str
    context: str
    channel: str
    persona: str
    pressure: str
    narrative: str
    message: Dict[str, Any]
    available_evidence: List[EvidenceItemScrubbed]
    available_actions: List[str] = [
        "PROCEED", "IGNORE", "REPLY_TO_SENDER", "VERIFY_INDEPENDENTLY",
        "REPORT", "ASK_TRUSTED_PERSON", "GATHER_MORE_EVIDENCE", "UNSURE"
    ]
