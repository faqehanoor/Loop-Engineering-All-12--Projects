import random
import time

FAILURE_RATE = 0.5
SIMULATED_WORK_TIME = 1

def run():
    """Simulates an unreliable operation that fails about half the time.

    Raises:
        RuntimeError: When the simulated operation fails.

    Returns:
        True when the operation succeeds.
    """
    time.sleep(SIMULATED_WORK_TIME)

    if random.random() < FAILURE_RATE:
        raise RuntimeError("Simulated operation failed")

    return True


if __name__ == "__main__":
    try:
        result = run()
        print(f"Task succeeded: {result}")
    except RuntimeError as e:
        print(f"Task failed: {e}")
