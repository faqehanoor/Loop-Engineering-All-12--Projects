import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from maker import run as run_maker
from checker import run as run_checker, generate_token, verify_token


TRANSCRIPT_DIR = "transcripts"


def write_transcript(name, result):
    """Write a transcript of a routine execution.

    Args:
        name: The routine name (e.g., 'maker' or 'checker').
        result: The result dict from the routine.

    Returns:
        The transcript string.
    """
    os.makedirs(TRANSCRIPT_DIR, exist_ok=True)

    lines = []
    lines.append("=" * 60)
    lines.append(f"ROUTINE TRANSCRIPT: {name.upper()}")
    lines.append("=" * 60)
    lines.append(f"Timestamp:  {datetime.now().isoformat()}")
    lines.append(f"Routine:    {name}")
    lines.append(f"Status:     {result['status'].upper()}")
    lines.append("-" * 60)
    lines.append("")

    lines.append(f"Task succeeded: {result['task_succeeded']}")
    lines.append(f"Message: {result['message']}")

    if result.get("result"):
        lines.append("")
        lines.append("Result details:")
        for key, value in result["result"].items():
            if key == "content":
                lines.append(f"  {key}: (see artifact file)")
            else:
                lines.append(f"  {key}: {value}")

    lines.append("")
    lines.append("-" * 60)

    if name == "maker":
        lines.append("HUMAN GATE: Review the artifact before approving Routine B.")
        lines.append("Do NOT automatically trigger Routine B.")
    elif name == "checker":
        lines.append("Routine B ran ONLY because it was explicitly triggered.")
        lines.append("The human gate was respected.")

    lines.append("=" * 60)

    transcript = "\n".join(lines)

    filepath = os.path.join(TRANSCRIPT_DIR, f"transcript_{name}.txt")
    with open(filepath, "w") as f:
        f.write(transcript)

    return transcript


def approve():
    """Record human approval in the state file."""
    state_file = "state.json"
    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            state = json.load(f)
    else:
        state = {}

    state["approved"] = True
    state["approved_timestamp"] = datetime.now().isoformat()

    with open(state_file, "w") as f:
        json.dump(state, f, indent=2)

    print("Human approval recorded.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_routine.py <maker|checker|approve|token>")
        print("  maker   - Run Routine A (create artifact)")
        print("  approve - Record human approval")
        print("  checker - Run Routine B (process artifact, requires prior approval)")
        print("  token   - Generate a new API trigger token")
        sys.exit(1)

    action = sys.argv[1]

    if action == "token":
        token = generate_token()
        print(f"API trigger token generated: {token}")
        print(f"Token saved to: checker_token.txt")
        print("Store this token securely. It will NOT be shown again.")
        return

    if action == "approve":
        approve()
        return

    if action == "maker":
        print("Running Routine A (Maker)...")
        result = run_maker()
    elif action == "checker":
        provided_token = sys.argv[2] if len(sys.argv) > 2 else None
        print("Running Routine B (Checker)...")
        result = run_checker(provided_token=provided_token)
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)

    print(f"Status: {result['status']}")
    print(f"Task succeeded: {result['task_succeeded']}")
    print(f"Message: {result['message']}")
    print()

    transcript = write_transcript(action, result)
    print("Transcript:")
    print(transcript)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nRoutine stopped by user.")
        sys.exit(0)
