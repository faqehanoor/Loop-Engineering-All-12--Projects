# Project 04 — Worker Queue Loop

A project demonstrating the producer-consumer pattern with a queue-based work distribution loop.

## What This Project Does

This project produces work items into a queue and dispatches them to multiple worker threads for processing. Workers pull items from the queue, process them (with simulated failures), and track results. A sentinel value signals workers to shut down gracefully when all items are processed.

## Files

- `work_item.py` - Simulates processing a single work item (~20% failure rate)
- `worker.py` - Worker function that pulls items from a queue and processes them
- `queue_loop.py` - Main loop: produces items, starts workers, collects results
- `test_queue.py` - Unit tests covering task processing, worker behavior, and queue loop
- `README.md` - This file

## How to Use

### Run the Queue Loop

```bash
cd project-04
python queue_loop.py
```

This produces 8 items and processes them with 2 workers. Example output:

```
Queue loop started. Items: 8, Workers: 2.
  Worker 1 started.
  Worker 2 started.
Producing 8 work items...
  Produced item 1.
  Produced item 2.
  ...
  [OK] Item 1 processed: task-1
  [FAIL] Failed to process item 3
  ...

Queue loop finished. 6 ok, 2 failed out of 8 items.
```

### Run the Work Item Standalone

```bash
python work_item.py
```

### Run the Tests

```bash
python -m pytest test_queue.py -v
```

## How the Queue Loop Works

The loop in `queue_loop.py` demonstrates these patterns:

1. **Queue-based distribution**: Uses `queue.Queue` for thread-safe work distribution
2. **Producer-consumer**: Main thread produces items, worker threads consume them
3. **Graceful shutdown**: Sends `None` sentinel to signal workers to stop
4. **Thread management**: Uses `threading.Thread` with `daemon=True` for background workers
5. **Result tracking**: Appends success/failure results to a shared list
6. **Clean completion**: Uses `queue.join()` to wait for all items to be processed

## Configuration

Constants at the top of `queue_loop.py`:

| Constant | Default | Description |
|----------|---------|-------------|
| `NUM_ITEMS` | 8 | Number of work items to produce |
| `NUM_WORKERS` | 2 | Number of worker threads |

## Stopping the Loop

Press `Ctrl+C` at any time to stop:

```
Queue loop stopped by user.
```

## Requirements

- Python 3.x
- No external packages required (uses only standard library modules)
- `pytest` for running tests (optional)
