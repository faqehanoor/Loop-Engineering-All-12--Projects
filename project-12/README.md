# Project 12 — Evidence-Based Improvement Loop Capstone

## What it does

Reads historical progress logs, detects repeated failures/corrections, collects evidence, and proposes the smallest rule change as a PR on a `claude/` branch. Requires human review before any changes are applied.

## Files

- `progress.md` - Historical run data with dated entries (12 weeks)
- `dreaming-state.md` - Tracks the last analyzed date
- `rules.md` - The rules file that could be improved (never auto-modified)
- `improvement_loop.py` - Main loop: detect patterns, propose changes
- `proposals/` - Generated proposals for human review
- `.gitignore` - Excludes generated files

## How to run

```bash
cd project-12
python improvement_loop.py
```

## Key concepts

- **Dreaming state**: A date marker — only entries after this date are analyzed
- **Pattern detection**: Finds corrections describing the same issue
- **Evidence-based**: Every proposal cites specific log entries and dates
- **Smallest change**: Proposes the minimum rule change needed
- **Human gate**: Rules.md is never auto-modified; proposals require review
