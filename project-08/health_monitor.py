import time
import sys
from health_service import check, recover

HEALTHY = "HEALTHY"
DEGRADED = "DEGRADED"
UNHEALTHY = "UNHEALTHY"

FAILURE_THRESHOLD = 3
RECOVERY_THRESHOLD = 2
MAX_CHECKS = 15
CHECK_INTERVAL = 1


class HealthMonitor:
    """Monitors service health with automatic recovery.

    States:
        HEALTHY: Service is operating normally.
        DEGRADED: Service is slow but responding.
        UNHEALTHY: Service is failing. Recovery is triggered.
    """

    def __init__(self, failure_threshold=FAILURE_THRESHOLD,
                 recovery_threshold=RECOVERY_THRESHOLD):
        self.state = HEALTHY
        self.failure_count = 0
        self.recovery_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_threshold = recovery_threshold
        self.recovery_attempts = 0
        self.history = []

    def _record(self, event, detail=""):
        self.history.append({"state": self.state, "event": event, "detail": detail})

    def check_health(self):
        """Perform a health check and update state.

        Returns:
            dict with 'success', 'state', 'message', and 'check_result'.
        """
        try:
            result = check()
        except ConnectionError as e:
            self.failure_count += 1
            self.recovery_count = 0
            if self.failure_count >= self.failure_threshold:
                if self.state != UNHEALTHY:
                    self.state = UNHEALTHY
                    self._record("unhealthy", f"failures={self.failure_count}")
                    self._attempt_recovery()
                else:
                    self._record("still_unhealthy", f"failures={self.failure_count}")
            else:
                self._record("failure", f"count={self.failure_count}/{self.failure_threshold}")
            return {
                "success": False,
                "state": self.state,
                "message": str(e),
                "check_result": None,
            }

        if result["status"] == "degraded":
            self.failure_count = 0
            self.recovery_count = 0
            if self.state != DEGRADED:
                self.state = DEGRADED
                self._record("degraded", f"response={result['response_time']}s")
            else:
                self._record("still_degraded", f"response={result['response_time']}s")
            return {
                "success": True,
                "state": self.state,
                "message": result["message"],
                "check_result": result,
            }

        self.failure_count = 0
        self.recovery_count += 1
        if self.state != HEALTHY:
            if self.recovery_count >= self.recovery_threshold:
                self.state = HEALTHY
                self._record("recovered", f"consecutive_ok={self.recovery_count}")
            else:
                self._record("improving", f"consecutive_ok={self.recovery_count}")
        else:
            self._record("ok", f"response={result['response_time']}s")
        return {
            "success": True,
            "state": self.state,
            "message": result["message"],
            "check_result": result,
        }

    def _attempt_recovery(self):
        """Attempt to recover an unhealthy service."""
        self.recovery_attempts += 1
        result = recover()
        if result["status"] == "recovered":
            self._record("recovery_success", result["message"])
        else:
            self._record("recovery_failed", result["message"])


def watchdog_loop():
    """Run the health monitoring loop.

    Returns:
        dict with summary of the monitoring session.
    """
    monitor = HealthMonitor()
    results = []

    print(f"Watchdog loop started.")
    print(f"  Failure threshold: {FAILURE_THRESHOLD}, Recovery threshold: {RECOVERY_THRESHOLD}")
    print(f"  Max checks: {MAX_CHECKS}, Check interval: {CHECK_INTERVAL}s")
    print(f"  Initial state: {monitor.state}")

    for i in range(1, MAX_CHECKS + 1):
        print(f"\nCheck {i}/{MAX_CHECKS}...")
        summary = monitor.check_health()
        results.append(summary)
        print(f"  [{summary['state']}] {summary['message']}")

        if i < MAX_CHECKS:
            time.sleep(CHECK_INTERVAL)

    healthy_checks = sum(1 for r in results if r["state"] == HEALTHY)
    unhealthy_checks = sum(1 for r in results if r["state"] == UNHEALTHY)
    degraded_checks = sum(1 for r in results if r["state"] == DEGRADED)
    recoveries = sum(1 for h in monitor.history if h["event"] == "recovery_success")

    print(f"\nWatchdog loop finished.")
    print(f"  Final state: {monitor.state}")
    print(f"  Checks: {healthy_checks} healthy, {degraded_checks} degraded, {unhealthy_checks} unhealthy")
    print(f"  Recovery attempts: {monitor.recovery_attempts} ({recoveries} succeeded)")

    return {
        "final_state": monitor.state,
        "healthy_checks": healthy_checks,
        "degraded_checks": degraded_checks,
        "unhealthy_checks": unhealthy_checks,
        "recovery_attempts": monitor.recovery_attempts,
        "results": results,
        "history": monitor.history,
    }


if __name__ == "__main__":
    try:
        summary = watchdog_loop()
        if summary["unhealthy_checks"] == 0:
            print("No unhealthy checks detected.")
        else:
            print(f"  {summary['unhealthy_checks']} check(s) detected as unhealthy.")
    except KeyboardInterrupt:
        print("\nWatchdog loop stopped by user.")
        sys.exit(0)
