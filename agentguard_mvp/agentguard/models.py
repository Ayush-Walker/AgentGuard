from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class ToolCall(BaseModel):
    action: str = Field(..., min_length=1)
    target: Optional[str] = None
    arguments: Dict[str, Any] = Field(default_factory=dict)
    agent_id: str = "demo-agent"

class DecisionRequest(BaseModel):
    decision: str
