import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from secret_check import run


TRANSCRIPT_FILE = "transcript.txt"


def write_transcript(mode, result):
    """Write a transcript of the secret check execution.

    Args:
        mode: The mode used ('env_file' or 'env_var').
        result: The result dict from secret_check.run().
    """
    lines = []
    lines.append("=" * 60)
    lines.append("SECRET CHECK TRANSCRIPT")
    lines.append("=" * 60)
    lines.append(f"Timestamp:  {datetime.now().isoformat()}")
    lines.append(f"Mode:       {mode}")
    lines.append(f"Status:     {result['status'].upper()}")
    lines.append("-" * 60)
    lines.append("")

    if result["method"] == "env_file":
        lines.append("ATTEMPT: Read token from local .env file")
    else:
        lines.append("ATTEMPT: Read token from environment variable")

    lines.append("")

    if result["result"]["success"]:
        lines.append(f"Token source: {result['result']['source']}")
        lines.append(f"Token value:  {result['result']['token']}")
    else:
        lines.append(f"Token source: {result['result']['source']}")
        lines.append(f"Error:        {result['result']['error']}")

    lines.append("")

    if result["verification"]:
        lines.append(f"Verification: {result['verification']['message']}")
    else:
        lines.append("Verification: SKIPPED (no token to verify)")

    lines.append("")
    lines.append("-" * 60)

    if result["task_succeeded"]:
        lines.append("TASK RESULT: SUCCESS")
        lines.append("The token was obtained and verified.")
    else:
        lines.append("TASK RESULT: FAILURE")
        if result["method"] == "env_file":
            lines.append("The local .env file was not available.")
            lines.append("This is expected in a fresh cloud clone because")
            lines.append("gitignored files are never pushed to GitHub.")
        else:
            lines.append("The environment variable was not set.")

    lines.append("")
    lines.append("KEY LESSON:")
    lines.append("Gitignored files never reach GitHub, so a fresh cloud")
    lines.append("clone does not contain them. Secrets required by a")
    lines.append("cloud routine must be supplied through environment")
    lines.append("variables, not by relying on a local .env file.")
    lines.append("=" * 60)

    transcript = "\n".join(lines)

    with open(TRANSCRIPT_FILE, "w") as f:
        f.write(transcript)

    return transcript


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_check.py <env_file|env_var>")
        sys.exit(1)

    mode = sys.argv[1]
    if mode not in ("env_file", "env_var"):
        print("Usage: python run_check.py <env_file|env_var>")
        sys.exit(1)

    use_env_var = mode == "env_var"
    print(f"Running secret check: mode={mode}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()

    result = run(use_env_var=use_env_var)

    print(f"Status: {result['status']}")
    print(f"Task succeeded: {result['task_succeeded']}")
    if result["result"].get("error"):
        print(f"Error: {result['result']['error']}")
    print()

    transcript = write_transcript(mode, result)
    print("Transcript:")
    print(transcript)
    print()
    print(f"Transcript saved to: {TRANSCRIPT_FILE}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSecret check stopped by user.")
        sys.exit(0)
