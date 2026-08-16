import random
import time

FAILURE_RATE = 0.7
WORK_TIME = 0.5


def call():
    """Simulates an unreliable API call.

    Returns:
        dict with 'status' and 'message' on success.

    Raises:
        ConnectionError: When the API call fails (simulates server error).
    """
    time.sleep(WORK_TIME)

    if random.random() < FAILURE_RATE:
        raise ConnectionError("API server error (503)")

    return {"status": "ok", "message": "API responded successfully"}


if __name__ == "__main__":
    try:
        result = call()
        print(f"[{result['status']}] {result['message']}")
    except ConnectionError as e:
        print(f"Error: {e}")
