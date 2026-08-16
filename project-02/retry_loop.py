import time
import sys
from flaky_task import run

MAX_RETRIES = 5
RETRY_DELAY = 2
TOTAL_TIMEOUT = 30


def retry_with_timeout():
    """Attempts the flaky task with retries and a total timeout.

    Returns:
        True if the task eventually succeeds, False otherwise.
    """
    start_time = time.time()

    print(f"Retry loop started. Max {MAX_RETRIES} attempts, {TOTAL_TIMEOUT}s timeout.")

    attempt = 1
    while attempt <= MAX_RETRIES:
        elapsed = time.time() - start_time
        if elapsed >= TOTAL_TIMEOUT:
            print(f"TIMEOUT: {TOTAL_TIMEOUT}s limit reached after {attempt - 1} attempts.")
            return False

        print(f"Attempt {attempt}/{MAX_RETRIES}...")
        try:
            result = run()
            print(f"SUCCESS: Task completed on attempt {attempt}.")
            return True
        except RuntimeError as e:
            print(f"FAILED: {e}")

        if attempt < MAX_RETRIES:
            remaining = TOTAL_TIMEOUT - elapsed
            wait = min(RETRY_DELAY, remaining)
            if wait > 0:
                print(f"Retrying in {wait:.0f}s...")
                time.sleep(wait)

        attempt += 1

    print(f"FAILED: All {MAX_RETRIES} attempts exhausted.")
    return False


if __name__ == "__main__":
    try:
        success = retry_with_timeout()
        if success:
            print("Retry loop ended successfully.")
        else:
            print("Retry loop ended with failure.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nRetry loop stopped by user.")
        sys.exit(0)
