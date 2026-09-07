from datetime import datetime, timezone
from uuid import uuid4
from typing import Any, Dict
from .models import ToolCall
from .policy import evaluate_tool_call

REQUESTS = []

def intercept(payload: Dict[str, Any]) -> Dict[str, Any]:
    tool_call = ToolCall.model_validate(payload)
    policy = evaluate_tool_call(tool_call.model_dump())
    if policy["risk"] == "GREEN":
        status = "allowed"
    elif policy["risk"] == "AMBER":
        status = "logged"
    else:
        status = "pending_approval"

    record = {
        "id": str(uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "payload": tool_call.model_dump(),
        **policy,
    }
    REQUESTS.insert(0, record)
    del REQUESTS[100:]
    return record

def decide(request_id: str, decision: str) -> Dict[str, Any]:
    if decision not in {"approve", "reject"}:
        raise ValueError("Decision must be approve or reject")
    for item in REQUESTS:
        if item["id"] == request_id:
            if item["risk"] != "RED":
                raise ValueError("Only red requests require human approval")
            item["status"] = "approved" if decision == "approve" else "rejected"
            item["decision"] = "ALLOW" if decision == "approve" else "BLOCK"
            item["decided_at"] = datetime.now(timezone.utc).isoformat()
            return item
    raise KeyError("Request not found")
