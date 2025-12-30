import pandas as pd
import random

data = []

for _ in range(600):
    sleep_hours = round(random.uniform(4, 9), 1)
    screen_time = round(random.uniform(2, 12), 1)
    work_hours = round(random.uniform(2, 12), 1)
    breaks = random.randint(1, 8)
    physical_activity = random.randint(0, 60)
    caffeine_intake = random.randint(0, 5)

    # Fatigue scoring logic
    fatigue_score = 0

    if sleep_hours < 6:
        fatigue_score += 2
    elif sleep_hours < 7:
        fatigue_score += 1

    if screen_time > 7:
        fatigue_score += 2
    elif screen_time > 5:
        fatigue_score += 1

    if work_hours > 8:
        fatigue_score += 2
    elif work_hours > 6:
        fatigue_score += 1

    if breaks < 3:
        fatigue_score += 1

    if physical_activity < 20:
        fatigue_score += 1

    if caffeine_intake > 3:
        fatigue_score += 1

    # Assign fatigue level
    if fatigue_score >= 6:
        fatigue_level = "High"
    elif fatigue_score >= 3:
        fatigue_level = "Medium"
    else:
        fatigue_level = "Low"

    data.append([
        sleep_hours,
        screen_time,
        work_hours,
        breaks,
        physical_activity,
        caffeine_intake,
        fatigue_level
    ])

# Create DataFrame
columns = [
    "sleep_hours",
    "screen_time",
    "work_hours",
    "breaks",
    "physical_activity",
    "caffeine_intake",
    "fatigue_level"
]

df = pd.DataFrame(data, columns=columns)

# Save dataset
df.to_csv("data/fatigue_data.csv", index=False)

print("✅ Realistic dataset with 600 rows generated successfully!")
