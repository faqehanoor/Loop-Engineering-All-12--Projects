# Project 09 — Routine Success vs Failure Drill

## What it does

Demonstrates that a "green" (completed) status does not necessarily mean the task succeeded. A routine runner executes a task, captures a transcript, and reports status. The infrastructure can complete successfully (GREEN) while the task itself fails.

## Files

- `routine.py` - File summarizer routine that reads a file and reports stats
- `run_routine.py` - One-off runner that executes the routine and captures a transcript
- `sample_data.txt` - Sample file for the successful run
- `transcript_success.txt` - Transcript from the successful run
- `transcript_failure.txt` - Transcript from the failed run

## How to run

```bash
cd project-09

# Successful run
python run_routine.py sample_data.txt

# Failed run (file does not exist)
python run_routine.py missing-file-that-does-not-exist.txt
```

## Key lesson

A green status means the session ended without an infrastructure error; it does not necessarily mean the requested task succeeded. Always check the transcript and actual task result.
