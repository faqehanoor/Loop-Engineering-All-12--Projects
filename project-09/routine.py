import os
import sys


def summarize_file(filepath):
    """Read a file and produce a summary of its contents.

    Args:
        filepath: Path to the file to summarize.

    Returns:
        dict with 'success', 'filename', 'lines', 'words', 'chars', 'preview'.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    with open(filepath, "r") as f:
        content = f.read()

    lines = content.strip().split("\n")
    words = content.split()
    preview = lines[0] if lines else "(empty file)"

    return {
        "success": True,
        "filename": os.path.basename(filepath),
        "lines": len(lines),
        "words": len(words),
        "chars": len(content),
        "preview": preview,
    }


def run(target_file):
    """Execute the file summarizer routine.

    Args:
        target_file: Path to the file to summarize.

    Returns:
        dict with 'status', 'task_succeeded', and 'result' or 'error'.
    """
    try:
        result = summarize_file(target_file)
        return {
            "status": "completed",
            "task_succeeded": True,
            "result": result,
            "error": None,
        }
    except FileNotFoundError as e:
        return {
            "status": "completed",
            "task_succeeded": False,
            "result": None,
            "error": str(e),
        }
    except Exception as e:
        return {
            "status": "completed",
            "task_succeeded": False,
            "result": None,
            "error": str(e),
        }
