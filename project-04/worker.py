import queue
from work_item import process

SENTINEL = None


def worker(work_queue, results):
    """Pulls items from the queue and processes them until shutdown.

    Args:
        work_queue: queue.Queue to pull items from.
        results: list to append result dicts to.
    """
    while True:
        try:
            item = work_queue.get(timeout=1)
        except queue.Empty:
            continue

        if item is SENTINEL:
            work_queue.task_done()
            break

        try:
            result = process(item)
            results.append(result)
            print(f"  [OK] {result['message']}")
        except RuntimeError as e:
            results.append({"id": item["id"], "status": "error", "message": str(e)})
            print(f"  [FAIL] {e}")
        finally:
            work_queue.task_done()
