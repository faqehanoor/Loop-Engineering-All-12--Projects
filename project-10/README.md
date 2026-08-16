# Project 10 — Secrets and Environment Variables Drill

## What it does

Demonstrates why secrets should be supplied via environment variables, not local `.env` files, when running in cloud environments. A `.env` file is gitignored and never reaches GitHub, so a fresh cloud clone cannot access it. Environment variables configured in the routine settings are always available.

## Files

- `.env` - Dummy token file (gitignored, not committed)
- `.gitignore` - Excludes `.env` from version control
- `secret_check.py` - Token verification routine with two modes
- `run_check.py` - Runner with transcript capture
- `transcript_env_file.txt` - Transcript from the local .env run
- `transcript_cloud_sim.txt` - Transcript from the simulated cloud run (no .env)
- `transcript_env_var.txt` - Transcript from the environment variable run

## How to run

```bash
cd project-10

# Part 1a: Local .env (works locally, fails in cloud)
python run_check.py env_file

# Part 1b: Simulated cloud (remove .env first, then run)
python run_check.py env_file

# Part 2: Environment variable (works everywhere)
$env:DUMMY_TOKEN="DUMMY_TOKEN_12345"   # PowerShell
python run_check.py env_var
```

## Key lesson

Gitignored files never reach GitHub, so a fresh cloud clone does not contain them. Secrets required by a cloud routine must be supplied through environment variables, not by relying on a local `.env` file.
