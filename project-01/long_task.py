import time
import os

print("Task started. Working for 2 minutes...")

# Wait for 2 minutes (120 seconds)
time.sleep(120)

# Create done.txt to signal completion
with open('done.txt', 'w') as f:
    f.write("Task completed successfully")

print("Task finished. done.txt created.")