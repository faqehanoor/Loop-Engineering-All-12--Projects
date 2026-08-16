import time
import sys
from api_service import call

CLOSED = "CLOSED"
OPEN = "OPEN"
HALF_OPEN = "HALF_OPEN"

FAILURE_THRESHOLD = 3
COOLDOWN = 5
MAX_CALLS = 12


class CircuitBreaker:
    """Manages circuit breaker state transitions.

    States:
        CLOSED: Normal operation. Failures are counted.
        OPEN: Circuit is tripped. Calls are rejected until cooldown expires.
        HALF_OPEN: Cooldown expired. One test call is allowed.
    """

    def __init__(self, failure_threshold=FAILURE_THRESHOLD, cooldown=COOLDOWN):
        self.state = CLOSED
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.cooldown = cooldown
        self.opened_at = 0.0
        self.history = []

    def _record(self, event, detail=""):
        self.history.append({"state": self.state, "event": event, "detail": detail})

    def _trip(self):
        self.state = OPEN
        self.opened_at = time.time()
        self._record("tripped", f"failures={self.failure_count}")

    def _reset(self):
        self.state = CLOSED
        self.failure_count = 0
        self._record("reset")

    def call_service(self):
        """Attempt a call through the circuit breaker.

        Returns:
            dict with 'success', 'state', 'message', and 'data' (if success).
        """
        if self.state == OPEN:
            elapsed = time.time() - self.opened_at
            if elapsed >= self.cooldown:
                self.state = HALF_OPEN
                self._record("half_open", f"cooldown expired ({elapsed:.1f}s)")
                print(f"  Circuit: OPEN -> HALF_OPEN (cooldown expired)")
            else:
                remaining = self.cooldown - elapsed
                self._record("rejected", f"cooldown {remaining:.1f}s remaining")
                return {
                    "success": False,
                    "state": OPEN,
                    "message": f"Circuit OPEN. Retry in {remaining:.1f}s.",
                    "data": None,
                }

        try:
            result = call()
            if self.state == HALF_OPEN:
                self._reset()
                print(f"  Circuit: HALF_OPEN -> CLOSED (test call succeeded)")
            else:
                self.failure_count = 0
                self._record("success")
            return {
                "success": True,
                "state": self.state,
                "message": result["message"],
                "data": result,
            }
        except ConnectionError as e:
            self.failure_count += 1
            if self.state == HALF_OPEN:
                self._trip()
                print(f"  Circuit: HALF_OPEN -> OPEN (test call failed)")
            elif self.failure_count >= self.failure_threshold:
                self._trip()
                print(f"  Circuit: CLOSED -> OPEN (threshold reached)")
            else:
                self._record("failure", f"count={self.failure_count}/{self.failure_threshold}")
            return {
                "success": False,
                "state": self.state,
                "message": str(e),
                "data": None,
            }


def circuit_loop():
    """Demonstrates the full circuit breaker lifecycle.

    Returns:
        dict with summary of the loop execution.
    """
    cb = CircuitBreaker()
    results = []

    print(f"Circuit breaker loop started.")
    print(f"  Failure threshold: {FAILURE_THRESHOLD}, Cooldown: {COOLDOWN}s, Max calls: {MAX_CALLS}")
    print(f"  Initial state: {cb.state}")

    for call_num in range(1, MAX_CALLS + 1):
        print(f"\nCall {call_num}/{MAX_CALLS}...")
        summary = cb.call_service()
        results.append(summary)
        print(f"  [{summary['state']}] {summary['message']}")

        if call_num < MAX_CALLS:
            time.sleep(1)

    succeeded = sum(1 for r in results if r["success"])
    failed = sum(1 for r in results if not r["success"])
    transitions = sum(1 for h in cb.history if h["event"] in ("tripped", "reset"))

    print(f"\nCircuit breaker loop finished.")
    print(f"  Final state: {cb.state}")
    print(f"  Calls: {succeeded} succeeded, {failed} rejected/failed")
    print(f"  State transitions: {transitions}")

    return {
        "final_state": cb.state,
        "succeeded": succeeded,
        "failed": failed,
        "transitions": transitions,
        "results": results,
        "history": cb.history,
    }


if __name__ == "__main__":
    try:
        summary = circuit_loop()
        if summary["failed"] == 0:
            print("All calls succeeded.")
        else:
            print(f"{summary['failed']} call(s) failed or were rejected.")
    except KeyboardInterrupt:
        print("\nCircuit breaker loop stopped by user.")
        sys.exit(0)
