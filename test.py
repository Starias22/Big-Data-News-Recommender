from datetime import datetime

# Given ISO 8601 formatted date string
date_str = "2024-06-12T12:23:33Z"

# Convert to datetime object (parse the 'Z' as UTC time)
dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")

# Convert datetime object to timestamp in seconds
timestamp_seconds = int(dt.timestamp())

# Extract year, month, day, hour, minute, and second
year = dt.year
month = dt.month
day = dt.day
hour = dt.hour
minute = dt.minute
second = dt.second

# Print results
print(f"Timestamp in seconds: {timestamp_seconds}")
print(f"Year: {year}")
print(f"Month: {month}")
print(f"Day: {day}")
print(f"Hour: {hour}")
print(f"Minute: {minute}")
print(f"Second: {second}")
