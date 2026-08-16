# Project 03 — Periodic Task Loop

A project demonstrating a repeating loop that runs a task at fixed intervals, tracking execution history and handling errors.

## What This Project Does

This project runs a simulated task on a fixed schedule (every 5 seconds), tracks success/failure history across runs, and handles errors gracefully within the long-running loop. It demonstrates the periodic scheduling pattern common in background workers, health checks, and monitoring systems.

## Files

- `scheduled_task.py` - Simulates a periodic task (~30% failure rate)
- `periodic_loop.py` - Scheduling loop that runs the task at fixed intervals
- `test_periodic.py` - Unit tests covering success, failure, and mixed scenarios
- `README.md` - This file

## How to Use

### Run the Periodic Loop

```bash
cd project-03
python periodic_loop.py
```

This will run the task 10 times at 5-second intervals. Example output:

```
Periodic loop started. Interval: 5s, Max runs: 10.

Run 1/10 at 23:38:52...
  OK: Task completed
  Totals: 1 ok, 0 failed
  Next run in 5s...

Run 2/10 at 23:38:57...
  FAILED: Task failed at 2026-08-16T23:38:58.123456
  Totals: 1 ok, 1 failed
  Next run in 5s...

...

Periodic loop finished. 7 ok, 3 failed out of 10 runs.
```

### Run the Task Standalone

```bash
python scheduled_task.py
```

### Run the Tests

```bash
python -m pytest test_periodic.py -v
```

## How the Periodic Loop Works

The loop in `periodic_loop.py` demonstrates these patterns:

1. **Fixed-interval scheduling**: Uses `time.sleep(INTERVAL)` between runs
2. **Run counter**: Uses `while run_num <= MAX_RUNS` to limit executions
3. **History tracking**: Records status of each run in a list
4. **Error handling**: Uses `try/except` to catch per-run failures without stopping the loop
5. **Graceful interruption**: Handles `Ctrl+C` with `try/except KeyboardInterrupt`

## Configuration

Constants at the top of `periodic_loop.py`:

| Constant | Default | Description |
|----------|---------|-------------|
| `INTERVAL` | 5 | Seconds between runs |
| `MAX_RUNS` | 10 | Total number of runs |

## Stopping the Loop

Press `Ctrl+C` at any time to stop:

```
Periodic loop stopped by user.
```

## Requirements

- Python 3.x
- No external packages required (uses only standard library modules)
- `pytest` for running tests (optional)
