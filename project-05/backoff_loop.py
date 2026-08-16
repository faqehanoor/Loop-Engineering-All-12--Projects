import time
import sys
import random
from flaky_service import call

MAX_ATTEMPTS = 6
BASE_DELAY = 1
MAX_BACKOFF = 16
JITTER = 0.5
TOTAL_TIMEOUT = 60


def backoff_with_jitter(delay):
    """Calculates jittered delay: random value within +/- JITTER of delay.

    Args:
        delay: The base delay to apply jitter to.

    Returns:
        float: The jittered delay value.
    """
    jitter_range = delay * JITTER
    return delay + random.uniform(-jitter_range, jitter_range)


def backoff_loop():
    """Calls the service with exponential backoff and jitter.

    Returns:
        dict with 'success', 'attempts', 'delays' list, and 'total_time'.
    """
    delays = []
    start_time = time.time()

    print(f"Backoff loop started. Max {MAX_ATTEMPTS} attempts, {TOTAL_TIMEOUT}s timeout.")
    print(f"  Base delay: {BASE_DELAY}s, Max backoff: {MAX_BACKOFF}s, Jitter: {JITTER}")

    attempt = 1
    while attempt <= MAX_ATTEMPTS:
        elapsed = time.time() - start_time
        if elapsed >= TOTAL_TIMEOUT:
            print(f"\nTIMEOUT: {TOTAL_TIMEOUT}s limit reached after {attempt - 1} attempts.")
            return {
                "success": False,
                "attempts": attempt - 1,
                "delays": delays,
                "total_time": elapsed,
            }

        print(f"\nAttempt {attempt}/{MAX_ATTEMPTS}...")
        try:
            result = call()
            elapsed = time.time() - start_time
            print(f"SUCCESS: {result['message']} ({elapsed:.1f}s elapsed)")
            return {
                "success": True,
                "attempts": attempt,
                "delays": delays,
                "total_time": elapsed,
            }
        except ConnectionError as e:
            print(f"FAILED: {e}")

        if attempt < MAX_ATTEMPTS:
            backoff_delay = min(BASE_DELAY * (2 ** (attempt - 1)), MAX_BACKOFF)
            jittered = max(0, backoff_with_jitter(backoff_delay))
            delays.append(jittered)
            elapsed = time.time() - start_time
            remaining = TOTAL_TIMEOUT - elapsed
            wait = min(jittered, remaining)
            if wait > 0:
                print(f"  Backoff: {backoff_delay:.1f}s base -> {wait:.1f}s jittered")
                time.sleep(wait)

        attempt += 1

    elapsed = time.time() - start_time
    print(f"\nFAILED: All {MAX_ATTEMPTS} attempts exhausted ({elapsed:.1f}s elapsed).")
    return {
        "success": False,
        "attempts": MAX_ATTEMPTS,
        "delays": delays,
        "total_time": elapsed,
    }


if __name__ == "__main__":
    try:
        summary = backoff_loop()
        print(f"\n--- Summary ---")
        print(f"  Success: {summary['success']}")
        print(f"  Attempts: {summary['attempts']}")
        print(f"  Delays: {[f'{d:.1f}s' for d in summary['delays']]}")
        print(f"  Total time: {summary['total_time']:.1f}s")
        if not summary["success"]:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nBackoff loop stopped by user.")
        sys.exit(0)
