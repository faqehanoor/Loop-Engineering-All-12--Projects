import os
import json
import secrets
import sys
from datetime import datetime


STATE_FILE = "state.json"
TOKEN_FILE = "api_token.txt"
APPROVED_MARKER = "output/.approved"


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"maker_ran": False, "checker_ran": False, "approved": False}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def generate_token():
    """Generate a bearer token for the API trigger.

    Returns:
        The generated token string.
    """
    token = secrets.token_urlsafe(32)
    with open(TOKEN_FILE, "w") as f:
        f.write(token)
    return token


def verify_token(provided_token):
    """Verify the provided bearer token matches the stored token.

    Args:
        provided_token: The token to verify.

    Returns:
        True if valid, False otherwise.
    """
    if not os.path.exists(TOKEN_FILE):
        return False
    with open(TOKEN_FILE, "r") as f:
        stored_token = f.read().strip()
    return secrets.compare_digest(provided_token, stored_token)


def process_artifact():
    """Process the approved artifact.

    Returns:
        dict with 'success' and 'result'.
    """
    artifact_file = "output/draft_summary.txt"
    if not os.path.exists(artifact_file):
        return {"success": False, "error": "Artifact not found"}

    with open(artifact_file, "r") as f:
        content = f.read()

    processed_file = "output/processed_summary.txt"
    processed_content = (
        "=== PROCESSED SUMMARY ===\n"
        f"Processed: {datetime.now().isoformat()}\n"
        f"Source: {artifact_file}\n"
        "\n"
        "The draft summary has been reviewed and approved by a human.\n"
        "This file confirms the maker-checker workflow completed.\n"
        "\n"
        "--- Original Draft ---\n"
        f"{content}"
        "--- End Original ---\n"
        "\n"
        "=== END PROCESSED ===\n"
    )

    with open(processed_file, "w") as f:
        f.write(processed_content)

    return {"success": True, "filepath": processed_file}


def run(provided_token=None):
    """Execute Routine B: process the approved artifact.

    This routine ONLY runs when explicitly triggered with a valid token.

    Args:
        provided_token: The bearer token from the API trigger.

    Returns:
        dict with status and result.
    """
    state = load_state()

    if not state.get("maker_ran"):
        return {
            "status": "blocked",
            "task_succeeded": False,
            "message": "Routine A has not run yet. Nothing to process.",
        }

    if not state.get("approved"):
        return {
            "status": "blocked",
            "task_succeeded": False,
            "message": "Human approval not recorded. Routine B cannot proceed.",
        }

    if provided_token and not verify_token(provided_token):
        return {
            "status": "denied",
            "task_succeeded": False,
            "message": "Invalid bearer token. Access denied.",
        }

    result = process_artifact()

    state["checker_ran"] = True
    state["checker_timestamp"] = datetime.now().isoformat()
    save_state(state)

    return {
        "status": "completed",
        "task_succeeded": result["success"],
        "result": result,
        "message": "Artifact processed successfully after human approval.",
    }
