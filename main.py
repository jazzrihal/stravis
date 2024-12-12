import streamlit
import requests
import dotenv
import os
import pandas

dotenv.load_dotenv()
STRAVA_ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")
STRAVA_ATHLETE_ID = os.getenv("STRAVA_ATHLETE_ID")

headers = {"Authorization": f"Bearer {STRAVA_ACCESS_TOKEN}"}
response = requests.get("https://strava.com/api/v3/athlete", headers=headers)
athlete_data = response.json()

first_name = athlete_data["firstname"]
last_name = athlete_data["lastname"]

streamlit.title(f"{first_name} {last_name}")

response = requests.get(f"https://strava.com/api/v3/athletes/{STRAVA_ATHLETE_ID}/stats", headers=headers)
stats_data = response.json()

run_totals = stats_data["recent_run_totals"]
run_count = run_totals["count"]
run_distance = run_totals["distance"]
run_moving_time = run_totals["moving_time"]
run_elevation = run_totals["elevation_gain"]
run_achievement_count = run_totals["achievement_count"]

if type(run_distance) == float:
    run_distance = round(run_distance / 1000, 2)
if type(run_moving_time) == int:
    run_moving_time = run_moving_time / 60
if type(run_elevation) == float:
    run_elevation = round(run_elevation, 2)

streamlit.header("Recent Runs")
col1, col2, col3 = streamlit.columns(3)
col1.metric("Count", str(run_count))
col2.metric("Distance", str(run_distance) + " km")
col3.metric("Moving Time", str(run_moving_time) + " mins")
col1.metric("Elevation Gain", str(run_elevation) + " m")
col2.metric("Achievement Count", str(run_achievement_count))

response = requests.get(f"https://strava.com/api/v3/athletes/{STRAVA_ATHLETE_ID}/activities", headers=headers)
activities_data = response.json()

distance_by_time = {}
avg_speed = {}
i = 0
for activity in activities_data:
    if activity.get("type") != "Run":
        continue
    
    i += 1
    distance = activity.get("distance") / 1000
    moving_time = activity.get("moving_time") / 60
    distance_by_time.update({moving_time: distance})
    
streamlit.scatter_chart(distance_by_time, x_label="Moving Time (mins)", y_label="Distance (km)")

activities_data