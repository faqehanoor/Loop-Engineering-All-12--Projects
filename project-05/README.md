# Project 05 — Exponential Backoff Loop

A project demonstrating exponential backoff with jitter for handling transient failures in unreliable services.

## What This Project Does

This project simulates an unreliable service call that fails frequently (transient errors) and wraps it in a retry loop with exponential backoff. Each retry waits progressively longer before attempting again, with random jitter to prevent thundering herd problems. A max backoff cap prevents runaway delays, and a total timeout prevents infinite retries.

## Files

- `flaky_service.py` - Simulates an unreliable service call (~60% failure rate)
- `backoff_loop.py` - Retry loop with exponential backoff, jitter, and timeout
- `test_backoff.py` - Unit tests covering success, failure, timeout, and backoff behavior
- `README.md` - This file

## How to Use

### Run the Backoff Loop

```bash
cd project-05
python backoff_loop.py
```

This retries the service call up to 6 times with exponential backoff. Example output:

```
Backoff loop started. Max 6 attempts, 60s timeout.
  Base delay: 1s, Max backoff: 16s, Jitter: 0.5

Attempt 1/6...
FAILED: Service unavailable (transient)
  Backoff: 1.0s base -> 0.9s jittered

Attempt 2/6...
FAILED: Service unavailable (transient)
  Backoff: 2.0s base -> 2.4s jittered

Attempt 3/6...
SUCCESS: Service responded successfully (4.8s elapsed)

--- Summary ---
  Success: True
  Attempts: 3
  Delays: ['0.9s', '2.4s']
  Total time: 4.8s
```

### Run the Service Standalone

```bash
python flaky_service.py
```

### Run the Tests

```bash
python -m pytest test_backoff.py -v
```

## How the Backoff Loop Works

The loop in `backoff_loop.py` demonstrates these patterns:

1. **Exponential backoff**: Delay doubles each attempt: `base_delay * 2^(attempt-1)`
2. **Jitter**: Random variation (+/- 50%) prevents synchronized retries
3. **Max backoff cap**: Caps delay at 16s to prevent excessive waits
4. **Total timeout**: Stops retrying after 60s regardless of attempts
5. **Graceful interruption**: Handles `Ctrl+C` with `try/except KeyboardInterrupt`

## Configuration

Constants at the top of `backoff_loop.py`:

| Constant | Default | Description |
|----------|---------|-------------|
| `MAX_ATTEMPTS` | 6 | Maximum retry attempts |
| `BASE_DELAY` | 1 | Initial delay in seconds |
| `MAX_BACKOFF` | 16 | Maximum delay cap in seconds |
| `JITTER` | 0.5 | Jitter range (±50% of delay) |
| `TOTAL_TIMEOUT` | 60 | Maximum total time in seconds |

## Backoff Schedule

| Attempt | Base Delay | Max Jittered |
|---------|-----------|-------------|
| 1 | 1s | ~0.5-1.5s |
| 2 | 2s | ~1-3s |
| 3 | 4s | ~2-6s |
| 4 | 8s | ~4-12s |
| 5 | 16s (capped) | ~8-16s |
| 6 | 16s (capped) | ~8-16s |

## Stopping the Loop

Press `Ctrl+C` at any time to stop:

```
Backoff loop stopped by user.
```

## Requirements

- Python 3.x
- No external packages required (uses only standard library modules)
- `pytest` for running tests (optional)
