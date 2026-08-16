import os
import json
import sys
from datetime import datetime


OUTPUT_DIR = "output"
ARTIFACT_FILE = os.path.join(OUTPUT_DIR, "draft_summary.txt")
STATE_FILE = "state.json"


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"maker_ran": False, "checker_ran": False, "approved": False}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def create_artifact():
    """Create a reviewable draft summary.

    Returns:
        dict with 'success', 'filepath', and 'content'.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    content = (
        "=== DRAFT SUMMARY ===\n"
        f"Generated: {datetime.now().isoformat()}\n"
        "\n"
        "Project Status:\n"
        "- Projects 01-08: Loop patterns (retry, circuit breaker, rate limiting, etc.)\n"
        "- Project 09: Routine success vs failure drill\n"
        "- Project 10: Secrets and environment variables drill\n"
        "- Project 11: Human gate and maker-checker pattern (this draft)\n"
        "\n"
        "Key Observations:\n"
        "1. Each project introduces a new resilience pattern\n"
        "2. Testing complexity increases with each project\n"
        "3. The course progresses from simple polling to state machines\n"
        "\n"
        "=== END DRAFT ===\n"
    )

    with open(ARTIFACT_FILE, "w") as f:
        f.write(content)

    return {"success": True, "filepath": ARTIFACT_FILE, "content": content}


def run():
    """Execute Routine A: create a reviewable artifact.

    Returns:
        dict with status and result.
    """
    result = create_artifact()

    state = load_state()
    state["maker_ran"] = True
    state["maker_timestamp"] = datetime.now().isoformat()
    state["artifact_file"] = result["filepath"]
    save_state(state)

    return {
        "status": "completed",
        "task_succeeded": result["success"],
        "result": result,
        "message": "Draft summary created. Awaiting human review and approval.",
    }
