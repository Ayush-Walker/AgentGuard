# AgentGuard — Autonomous AI Agent Runtime Security & Action Gateway

A complete hackathon MVP with:
- JSON tool-call interceptor middleware
- Green / Amber / Red policy engine
- Prompt-injection detection
- FastAPI backend
- Streamlit live security dashboard
- Human-in-the-loop approval/rejection for Red actions
- Demo scenarios for judges

## 1. Install

```bash
python -m venv .venv
```

Windows:
```bash
.venv\\Scripts\\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

## 2. Run (one command)

```bash
python start.py
```

This starts the API on `http://127.0.0.1:8000` and opens the Streamlit dashboard.

## 3. Judge demo flow

1. Click **Safe: read_file** → Green → immediately allowed.
2. Click **Monitored: update_user** → Amber → logged for audit.
3. Click **Blocked: drop_database_table** → Red → status becomes Pending Approval.
4. Click **Approve** or **Reject** → human decision is recorded in the dashboard.
5. Click **Blocked: prompt injection** → policy engine detects a malicious instruction and blocks it.

## API

`POST /api/tool-call`

Example:
```json
{
  "action": "drop_database_table",
  "target": "customers",
  "arguments": {"cascade": true},
  "agent_id": "demo-agent"
}
```

`GET /api/requests`

`POST /api/requests/{request_id}/decision`
```json
{"decision":"approve"}
```

`GET /api/health`

## Security note

This MVP simulates tool execution and does **not** execute destructive commands. Approval changes the authorization state only, making it safe to demonstrate live interception and human-in-the-loop control.
