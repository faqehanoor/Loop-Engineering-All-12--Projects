# Project 11 — Human Gate and Maker-Checker Pattern Drill

## What it does

Demonstrates the human gate and maker-checker pattern. Routine A (Maker) creates a reviewable artifact. Routine B (Checker) processes it, but ONLY when explicitly triggered by a human after reviewing Routine A's result. Routine B is protected by a bearer token.

## Files

- `maker.py` - Routine A: creates a draft summary artifact
- `checker.py` - Routine B: processes the artifact after human approval + valid token
- `run_routine.py` - Runner for both routines with transcript capture
- `.gitignore` - Excludes tokens, state, and output files
- `transcripts/` - Saved transcripts from each run

## How to run

```bash
cd project-11

# Step 1: Run Routine A (Maker)
python run_routine.py maker

# Step 2: Review the artifact in output/draft_summary.txt

# Step 3: Approve the artifact
python run_routine.py approve

# Step 4: Generate API token
python run_routine.py token

# Step 5: Run Routine B (Checker) with the token
python run_routine.py checker <token>
```

## Key concepts

- **Human gate**: Routine B cannot run without explicit human approval
- **Maker-checker pattern**: One routine creates, another acts after review
- **Bearer token**: API trigger protected by a generated token
- **State file**: Tracks workflow progress (maker ran, approved, checker ran)
