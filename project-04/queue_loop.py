import queue
import threading
import sys
from worker import worker, SENTINEL

NUM_ITEMS = 8
NUM_WORKERS = 2


def queue_loop():
    """Produces work items, dispatches them to workers, and tracks results.

    Returns:
        dict with 'completed', 'failed', and 'results' list.
    """
    work_queue = queue.Queue()
    results = []

    print(f"Queue loop started. Items: {NUM_ITEMS}, Workers: {NUM_WORKERS}.")

    workers = []
    for i in range(NUM_WORKERS):
        t = threading.Thread(target=worker, args=(work_queue, results), daemon=True)
        t.start()
        workers.append(t)
        print(f"  Worker {i + 1} started.")

    print(f"Producing {NUM_ITEMS} work items...")
    for item_id in range(1, NUM_ITEMS + 1):
        item = {"id": item_id, "data": f"task-{item_id}"}
        work_queue.put(item)
        print(f"  Produced item {item_id}.")

    work_queue.join()

    for _ in workers:
        work_queue.put(SENTINEL)
    for t in workers:
        t.join()

    completed = sum(1 for r in results if r["status"] == "ok")
    failed = sum(1 for r in results if r["status"] == "error")

    print(f"\nQueue loop finished. {completed} ok, {failed} failed out of {NUM_ITEMS} items.")
    return {"completed": completed, "failed": failed, "results": results}


if __name__ == "__main__":
    try:
        summary = queue_loop()
        if summary["failed"] == 0:
            print("All items processed successfully.")
        else:
            print(f"{summary['failed']} item(s) failed.")
    except KeyboardInterrupt:
        print("\nQueue loop stopped by user.")
        sys.exit(0)
