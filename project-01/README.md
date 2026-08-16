# Project 01 — In-Session Completion Loop

A simple project demonstrating how to monitor a long-running task using a polling loop.

## What This Project Does

This project simulates a long-running task and monitors its completion using a simple polling loop. The task waits for 2 minutes and then creates a `done.txt` file to signal completion. The monitoring loop checks for this file every minute and stops when it detects the task has finished.

## Files

- `long_task.py` - Simulates a long-running task (waits 2 minutes, then creates `done.txt`)
- `loop.py` - Monitoring loop that checks for `done.txt` every minute
- `README.md` - This file

## How to Use

### Step 1: Start the Long-Running Task

Open a terminal and run:

```bash
python long_task.py
```

This will start the task and display:
```
Task started. Working for 2 minutes...
```

The task will wait for 2 minutes before creating `done.txt`.

### Step 2: Start the Monitoring Loop

Open a second terminal and run:

```bash
python loop.py
```

This will start monitoring and display:
```
Monitoring loop started. Checking every minute...
Task still running... checking again in 1 minute.
```

### Step 3: Wait for Completion

The monitoring loop will check once per minute. After 2 minutes, when `done.txt` is created, you'll see:

```
SUCCESS: Task completed! done.txt found.
Monitoring loop ended.
```

## How the Loop Works

The monitoring loop in `loop.py` uses a simple polling pattern:

1. **Infinite loop**: Uses `while True` to keep checking
2. **File existence check**: Uses `os.path.exists('done.txt')` to check if the task is done
3. **Sleep interval**: Uses `time.sleep(60)` to wait 1 minute between checks
4. **Clean exit**: Uses `break` to exit the loop when `done.txt` is found
5. **Graceful interruption**: Handles `Ctrl+C` with a `try/except KeyboardInterrupt`

## Stopping the Loop

You can stop the monitoring loop at any time by pressing `Ctrl+C`. This will display:
```
Monitoring stopped by user.
```

## Requirements

- Python 3.x
- No external packages required (uses only standard library modules)

## Project Structure

This is designed as a throwaway project for learning purposes. No persistent state or configuration files are created beyond the `done.txt` completion marker.