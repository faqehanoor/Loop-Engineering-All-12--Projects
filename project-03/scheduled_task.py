import random
import time
from datetime import datetime

FAILURE_RATE = 0.3
WORK_TIME = 1


def run():
    """Simulates a periodic task that occasionally fails.

    Returns:
        dict with 'status' ('ok' or 'error'), 'timestamp', and 'message'.

    Raises:
        RuntimeError: When the simulated task fails.
    """
    time.sleep(WORK_TIME)
    now = datetime.now().isoformat()

    if random.random() < FAILURE_RATE:
        raise RuntimeError(f"Task failed at {now}")

    return {"status": "ok", "timestamp": now, "message": "Task completed"}


if __name__ == "__main__":
    try:
        result = run()
        print(f"[{result['timestamp']}] {result['message']}")
    except RuntimeError as e:
        print(f"Error: {e}")
