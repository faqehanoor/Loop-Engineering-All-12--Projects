import random
import time

FAILURE_RATE = 0.6
WORK_TIME = 0.5


def call():
    """Simulates an unreliable service call that fails often.

    Returns:
        dict with 'status' and 'message' on success.

    Raises:
        ConnectionError: When the service call fails (transient error).
    """
    time.sleep(WORK_TIME)

    if random.random() < FAILURE_RATE:
        raise ConnectionError("Service unavailable (transient)")

    return {"status": "ok", "message": "Service responded successfully"}


if __name__ == "__main__":
    try:
        result = call()
        print(f"[{result['status']}] {result['message']}")
    except ConnectionError as e:
        print(f"Error: {e}")
