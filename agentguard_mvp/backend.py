from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from agentguard.interceptor import REQUESTS, intercept, decide
from agentguard.models import DecisionRequest

app = FastAPI(title="AgentGuard API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "AgentGuard"}

@app.post("/api/tool-call")
def tool_call(payload: dict):
    try:
        return intercept(payload)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=str(exc))

@app.get("/api/requests")
def requests():
    return {"items": REQUESTS}

@app.post("/api/requests/{request_id}/decision")
def request_decision(request_id: str, body: DecisionRequest):
    try:
        return decide(request_id, body.decision.lower())
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
