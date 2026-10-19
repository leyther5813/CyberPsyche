from pydantic import BaseModel
from typing import Dict, Any, Optional

class BehaviourEventDTO(BaseModel):
    scenario_id: str
    event_type: str  # view | open_evidence | action | reason | confidence
    payload: Optional[Dict[str, Any]] = None
    ts: Optional[str] = None
