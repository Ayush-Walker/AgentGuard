import json
import re
from typing import Any, Dict

GREEN_ACTIONS = {
    "read", "read_file", "get", "get_user", "get_status", "list", "list_files",
    "search", "search_docs", "fetch", "fetch_url", "view", "health_check"
}
AMBER_ACTIONS = {
    "write", "write_file", "create_file", "update", "update_user", "edit",
    "send_email", "send_message", "create_ticket", "deploy_preview", "change_setting"
}
RED_ACTIONS = {
    "drop_database_table", "drop_table", "delete_database", "delete_db",
    "delete_file", "delete_user", "revoke_credentials", "rotate_all_keys",
    "shutdown_server", "wipe_storage", "format_disk", "disable_security",
    "execute_shell", "run_command", "destroy_environment", "exfiltrate_secrets"
}

PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+(the\s+)?system\s+prompt",
    r"reveal\s+(the\s+)?system\s+prompt",
    r"show\s+(me\s+)?(the\s+)?api\s*key",
    r"reveal\s+(the\s+)?secret",
    r"disable\s+(security|guard|agentguard)",
    r"bypass\s+(security|policy|approval)",
    r"do\s+not\s+log",
]

DANGEROUS_SHELL_PATTERNS = [
    r"rm\s+-rf", r"del\s+/[sqf]", r"format\s+[a-z]:", r"shutdown",
    r"curl\s+.*\|\s*(bash|sh)", r"wget\s+.*\|\s*(bash|sh)",
    r"powershell\s+.*-enc"
]

def _contains_pattern(text: str, patterns) -> bool:
    return any(re.search(p, text, re.I) for p in patterns)

def evaluate_tool_call(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = str(payload.get("action", "")).strip().lower()
    blob = json.dumps(payload, ensure_ascii=False, default=str)
    injection = _contains_pattern(blob, PROMPT_INJECTION_PATTERNS)
    shell_danger = action in {"execute_shell", "run_command"} and _contains_pattern(blob, DANGEROUS_SHELL_PATTERNS)

    if action in RED_ACTIONS or injection or shell_danger:
        reasons = []
        if action in RED_ACTIONS:
            reasons.append(f"Action '{action}' is classified as destructive/high-risk.")
        if injection:
            reasons.append("Prompt-injection/security-bypass pattern detected.")
        if shell_danger:
            reasons.append("Dangerous shell command pattern detected.")
        return {"risk": "RED", "risk_score": 95, "decision": "BLOCK", "reason": " ".join(reasons)}

    if action in GREEN_ACTIONS:
        return {"risk": "GREEN", "risk_score": 10, "decision": "ALLOW", "reason": "Read-only/benign action matched the allow policy."}

    if action in AMBER_ACTIONS:
        return {"risk": "AMBER", "risk_score": 50, "decision": "LOG", "reason": "Action is consequential but not inherently destructive; logged for audit."}

    return {"risk": "AMBER", "risk_score": 45, "decision": "LOG", "reason": "Unknown action defaults to monitored/amber policy."}
