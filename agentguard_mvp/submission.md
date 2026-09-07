# AgentGuard — Hackathon Submission

## Problem
Autonomous AI agents can make tool calls that affect databases, files, credentials, infrastructure, or external systems. A runtime security layer is needed to intercept and control these actions before execution.

## Solution
AgentGuard is middleware between an AI agent and its tools. Every tool-call JSON payload is validated, classified by a policy engine, logged, and either allowed, monitored, or held for human approval.

## Core features
- Live JSON interception
- Green / Amber / Red policy classification
- Destructive-action blocking
- Prompt-injection and security-bypass detection
- Real-time monitoring dashboard
- Human approval/rejection workflow
- Audit-friendly request history

## Tech stack
Python, FastAPI, Pydantic, Streamlit, Requests

## Demo
Use the four demo buttons in the dashboard to demonstrate safe, monitored, destructive, and prompt-injection tool calls.
