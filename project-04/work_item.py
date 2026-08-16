import random
import time

FAILURE_RATE = 0.2
PROCESS_TIME = 0.5


def process(item):
    """Processes a work item. Fails randomly to simulate unreliable work.

    Args:
        item: A dict with 'id' and 'data' keys.

    Returns:
        dict with 'id', 'status' ('ok' or 'error'), and 'message'.

    Raises:
        RuntimeError: When processing fails.
    """
    time.sleep(PROCESS_TIME)

    if random.random() < FAILURE_RATE:
        raise RuntimeError(f"Failed to process item {item['id']}")

    return {
        "id": item["id"],
        "status": "ok",
        "message": f"Item {item['id']} processed: {item['data']}",
    }


if __name__ == "__main__":
    test_item = {"id": 1, "data": "test work"}
    try:
        result = process(test_item)
        print(f"[{result['status']}] {result['message']}")
    except RuntimeError as e:
        print(f"Error: {e}")
