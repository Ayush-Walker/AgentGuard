# AgentGuard — Autonomous AI Agent Runtime Security & Action Gateway

**Problem Statement:** CC-GFG-01
**Hackathon:** Career Catalyst Club × GeeksforGeeks — 4-Hour Software Hackathon

## Overview

AgentGuard is a runtime security middleware and monitoring dashboard designed to protect AI agents that use tool-calling capabilities.

AI agents can accidentally or maliciously perform dangerous operations such as deleting database tables or modifying sensitive information. AgentGuard intercepts simulated tool-call JSON payloads, evaluates the requested action using a policy engine, and assigns a risk level:

* 🟢 **Green — Allowed:** Safe actions are permitted immediately.
* 🟠 **Amber — Logged:** Medium-risk actions are recorded for monitoring.
* 🔴 **Red — Approval Required:** Destructive or high-risk actions require human authorization.

## Key Features

* Tool-call JSON interception and parsing
* Runtime policy-based risk classification
* Green / Amber / Red security categories
* Human-in-the-loop approval for destructive actions
* Real-time Streamlit security monitoring dashboard
* Clear visibility of agent actions and their security status
* Lightweight architecture suitable for local execution

## Architecture

```text
AI Agent / Simulated Tool Call
            ↓
      JSON Payload
            ↓
    AgentGuard Interceptor
            ↓
       Policy Engine
       ↙     ↓      ↘
   GREEN   AMBER    RED
  Allowed  Logged   Approval
                     ↓
              Human Decision
                 ↙       ↘
             Approve     Reject
```

## Example Tool Calls

### Safe action

```json
{
  "tool": "read_file",
  "arguments": {
    "path": "report.txt"
  }
}
```

Result: **GREEN — Allowed**

### Medium-risk action

```json
{
  "tool": "update_user",
  "arguments": {
    "user_id": 101
  }
}
```

Result: **AMBER — Logged**

### Destructive action

```json
{
  "tool": "drop_database_table",
  "arguments": {
    "table": "users"
  }
}
```

Result: **RED — Requires human approval**

## Technology Stack

* Python
* Streamlit
* JSON
* Python standard libraries

## Installation

Clone the repository:

```bash
git clone https://github.com/Ayush-Walker/AgentGuard.git
cd AgentGuard
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the Streamlit dashboard:

```bash
streamlit run dashboard.py
```

If the project uses the provided start script, it can also be launched using:

```bash
python start.py
```

## Project Structure

```text
AgentGuard/
├── backend.py
├── dashboard.py
├── start.py
├── requirements.txt
├── README.md
└── submission/
```

## Hackathon MVP Demonstration

The application demonstrates the required CC-GFG-01 workflow:

1. A benign `read_file` action passes immediately.
2. An `update_user` action is logged for monitoring.
3. A destructive `drop_database_table` action is classified as RED.
4. The dashboard requests human authorization.
5. The human can approve or reject the action.

## Responsible Use

AgentGuard is intended as a defensive runtime security layer for AI agents. It should be used to prevent unauthorized or destructive agent behavior and should not be used for malicious activities.

## Future Improvements

* Regex-based prompt injection detection
* More granular policy rules
* Webhook notifications through Slack or Discord
* Persistent audit logs
* Authentication and role-based approval
* More advanced policy configuration

## Team

Built for the **Career Catalyst Club × GeeksforGeeks Software Hackathon**.

**Problem Statement:** CC-GFG-01 — AgentGuard
