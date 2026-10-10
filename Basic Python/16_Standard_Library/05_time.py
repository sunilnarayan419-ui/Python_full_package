"""
TOPIC: time
MAIN POINTS:
- Read timestamps.
- Pause execution with sleep().
- Measure elapsed execution time with perf_counter().
"""

import time

# Current Unix timestamp
print("Unix timestamp:", time.time())

# Measure execution duration
start_time = time.perf_counter()

total = sum(range(1_000_000))

end_time = time.perf_counter()

print("Calculation result:", total)
print("Elapsed seconds:", end_time - start_time)

# Pause execution
print("Starting a short pause...")
time.sleep(1)
print("Pause completed.")

# time.sleep() is useful for demonstrations and simple delays.
# For production scheduling, use an appropriate scheduler.