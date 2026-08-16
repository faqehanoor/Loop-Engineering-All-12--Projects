# Project 02 — Retry/Timeout Loop

A project demonstrating retry logic with a total timeout for handling unreliable operations.

## What This Project Does

This project simulates an unreliable operation that fails randomly and wraps it in a retry loop with configurable maximum attempts and a total timeout. The retry loop attempts the operation up to N times, waits between retries, and gives up if the total time exceeds a timeout limit.

## Files

- `flaky_task.py` - Simulates an unreliable operation (fails ~50% of the time)
- `retry_loop.py` - Retry loop with max attempts and total timeout
- `test_retry.py` - Unit tests covering success, failure, and timeout conditions
- `README.md` - This file

## How to Use

### Run the Retry Loop

```bash
cd project-02
python retry_loop.py
```

This will attempt the flaky task up to 5 times with a 30-second timeout. Example output:

```
Retry loop started. Max 5 attempts, 30s timeout.
Attempt 1/5...
FAILED: Simulated operation failed
Retrying in 2s...
Attempt 2/5...
FAILED: Simulated operation failed
Retrying in 2s...
Attempt 3/5...
SUCCESS: Task completed on attempt 3.
Retry loop ended successfully.
```

### Run the Flaky Task Standalone

```bash
python flaky_task.py
```

### Run the Tests

```bash
python -m pytest test_retry.py -v
```

## How the Retry Loop Works

The retry loop in `retry_loop.py` demonstrates these patterns:

1. **Retry counter**: Uses `while attempt <= MAX_RETRIES` to limit attempts
2. **Timeout check**: Compares elapsed time against `TOTAL_TIMEOUT` each iteration
3. **Error handling**: Uses `try/except` to catch task failures
4. **Clean exit**: Uses `return True/False` to signal success or failure
5. **Graceful interruption**: Handles `Ctrl+C` with `try/except KeyboardInterrupt`

## Configuration

Constants at the top of `retry_loop.py`:

| Constant | Default | Description |
|----------|---------|-------------|
| `MAX_RETRIES` | 5 | Maximum number of retry attempts |
| `RETRY_DELAY` | 2 | Seconds to wait between retries |
| `TOTAL_TIMEOUT` | 30 | Maximum total time in seconds |

## Stopping the Loop

Press `Ctrl+C` at any time to stop:

```
Retry loop stopped by user.
```

## Requirements

- Python 3.x
- No external packages required (uses only standard library modules)
- `pytest` for running tests (optional)
