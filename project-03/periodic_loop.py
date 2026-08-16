import time
import sys
from datetime import datetime
from scheduled_task import run

INTERVAL = 5
MAX_RUNS = 10


def periodic_loop():
    """Runs the scheduled task at fixed intervals, tracking execution history.

    Returns:
        dict with 'success_count', 'fail_count', and 'history' list.
    """
    history = []
    success_count = 0
    fail_count = 0

    print(f"Periodic loop started. Interval: {INTERVAL}s, Max runs: {MAX_RUNS}.")

    run_num = 1
    while run_num <= MAX_RUNS:
        print(f"\nRun {run_num}/{MAX_RUNS} at {datetime.now().strftime('%H:%M:%S')}...")

        try:
            result = run()
            success_count += 1
            entry = {"run": run_num, "status": "ok", "message": result["message"]}
            history.append(entry)
            print(f"  OK: {result['message']}")
        except RuntimeError as e:
            fail_count += 1
            entry = {"run": run_num, "status": "error", "message": str(e)}
            history.append(entry)
            print(f"  FAILED: {e}")

        print(f"  Totals: {success_count} ok, {fail_count} failed")

        if run_num < MAX_RUNS:
            print(f"  Next run in {INTERVAL}s...")
            time.sleep(INTERVAL)

        run_num += 1

    print(f"\nPeriodic loop finished. {success_count} ok, {fail_count} failed out of {MAX_RUNS} runs.")
    return {"success_count": success_count, "fail_count": fail_count, "history": history}


if __name__ == "__main__":
    try:
        summary = periodic_loop()
        if summary["fail_count"] == 0:
            print("All runs succeeded.")
        else:
            print(f"{summary['fail_count']} run(s) failed.")
    except KeyboardInterrupt:
        print("\nPeriodic loop stopped by user.")
        sys.exit(0)
