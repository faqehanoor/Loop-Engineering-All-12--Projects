import time
import os
import sys

print("Monitoring loop started. Checking every minute...")

try:
    while True:
        # Check if done.txt exists
        if os.path.exists('done.txt'):
            print("SUCCESS: Task completed! done.txt found.")
            break
        else:
            # Task still running, wait 1 minute before checking again
            print("Task still running... checking again in 1 minute.")
            time.sleep(60)
except KeyboardInterrupt:
    # Handle Ctrl+C gracefully
    print("\nMonitoring stopped by user.")
    sys.exit(0)

print("Monitoring loop ended.")