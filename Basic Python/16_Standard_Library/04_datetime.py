"""
TOPIC: datetime
MAIN POINTS:
- Work with dates and times.
- Format dates as strings.
- Parse date strings.
- Calculate time differences.
"""

from datetime import date, datetime, timedelta

# Current date and time
now = datetime.now()
today = date.today()

print("Current date:", today)
print("Current date and time:", now)

# Format a date
formatted_date = now.strftime("%d-%m-%Y %H:%M:%S")
print("Formatted date:", formatted_date)

# Parse a date string
experiment_date = datetime.strptime(
    "2026-10-11", "%Y-%m-%d"
)
print("Experiment date:", experiment_date)

# Date arithmetic
follow_up_date = experiment_date + timedelta(days=14)
print("Follow-up date:", follow_up_date.date())

# Calculate duration
start = datetime(2026, 10, 1)
end = datetime(2026, 10, 11)
print("Days between dates:", (end - start).days)

# For timestamps across time zones, explore datetime.timezone
# and the zoneinfo module.