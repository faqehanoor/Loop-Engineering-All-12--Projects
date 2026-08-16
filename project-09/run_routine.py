import os
import sys
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from routine import run


TRANSCRIPT_FILE = "transcript.txt"


def write_transcript(target_file, result):
    """Write a transcript of the routine execution.

    Args:
        target_file: The file that was targeted.
        result: The result dict from routine.run().
    """
    lines = []
    lines.append("=" * 60)
    lines.append("ROUTINE TRANSCRIPT")
    lines.append("=" * 60)
    lines.append(f"Timestamp:  {datetime.now().isoformat()}")
    lines.append(f"Target:     {target_file}")
    lines.append(f"Status:     {result['status'].upper()}")
    lines.append("-" * 60)
    lines.append("")

    if result["task_succeeded"]:
        lines.append("TASK RESULT: SUCCESS")
        lines.append("")
        r = result["result"]
        lines.append(f"  File:     {r['filename']}")
        lines.append(f"  Lines:    {r['lines']}")
        lines.append(f"  Words:    {r['words']}")
        lines.append(f"  Chars:    {r['chars']}")
        lines.append(f"  Preview:  {r['preview']}")
    else:
        lines.append("TASK RESULT: FAILURE")
        lines.append("")
        lines.append(f"  Error:    {result['error']}")

    lines.append("")
    lines.append("-" * 60)
    lines.append(f"Infrastructure status: GREEN (routine completed without crash)")
    lines.append("=" * 60)

    transcript = "\n".join(lines)

    with open(TRANSCRIPT_FILE, "w") as f:
        f.write(transcript)

    return transcript


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_routine.py <target_file>")
        sys.exit(1)

    target_file = sys.argv[1]
    print(f"Running routine against: {target_file}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()

    result = run(target_file)

    print(f"Status: {result['status']}")
    print(f"Task succeeded: {result['task_succeeded']}")
    if result["error"]:
        print(f"Error: {result['error']}")
    print()

    transcript = write_transcript(target_file, result)
    print("Transcript:")
    print(transcript)
    print()
    print(f"Transcript saved to: {TRANSCRIPT_FILE}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nRoutine stopped by user.")
        sys.exit(0)
