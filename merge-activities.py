#!/home/henning/github/python-garminconnect/.venv/bin/python merge-last-activity.py
"""
Fetches the last n activities, optionally with their splits, and race predictions using the Garmin API.

This script uses the python-garminconnect library to fetch the most recent activities,
along with their splits (if requested and available) and race predictions. It combines them into a
single JSON object and prints it to stdout.

It reuses the API initialization logic from demo.py to handle authentication.
"""

import argparse
import json
import sys

# Import the API initialization function and configuration from demo.py
# This allows us to reuse the robust authentication and token handling.
from demo import init_api, config


def main():
    """
    Main function to fetch and combine Garmin Connect data for the last n activities.
    """
    parser = argparse.ArgumentParser(description="Fetch the last n activities from Garmin Connect with optional splits and race predictions.")
    parser.add_argument("n", type=int, default=1, nargs="?", help="Number of recent activities to fetch (default: 1)")
    parser.add_argument("--include-splits", action="store_true", help="Include activity splits in the output")
    args = parser.parse_args()
    n = args.n
    include_splits = args.include_splits

    # Initialize the Garmin API. This will handle login, token refresh, and MFA.
    # We pass credentials as None to use environment variables or prompt the user.
    # Enable CLI mode to print messages to stderr instead of stdout
    config.is_cli_mode = True
    print("Initializing Garmin Connect API...", file=sys.stderr)
    api = init_api(email=None, password=None)

    if not api:
        print("API initialization failed. Exiting.", file=sys.stderr)
        sys.exit(1)

    try:
        print(f"Fetching last {n} activities...", file=sys.stderr)
        activities_data = api.get_activities(0, n)

        # Extract the list of activities from the response
        if isinstance(activities_data, list):
            activities_list = activities_data
        elif isinstance(activities_data, dict) and "activityList" in activities_data:
            activities_list = activities_data["activityList"]
        else:
            activities_list = []

        # Fetch splits for each activity
        activities_with_splits = []
        for activity in activities_list:
            splits = {}
            if include_splits:
                activity_id = activity.get("activityId")
                if activity_id:
                    print(f"Fetching splits for activity ID: {activity_id}", file=sys.stderr)
                    splits = api.get_activity_splits(activity_id) or {}
            activities_with_splits.append({
                "activity": activity,
                "splits": splits
            })

        print("Fetching race predictions...", file=sys.stderr)
        # Get race predictions for the date range of the activities
        if activities_list:
            from_date = activities_list[-1]["startTimeGMT"].split(" ")[0]
            to_date = activities_list[0]["startTimeGMT"].split(" ")[0]
            race_predictions = api.get_race_predictions(startdate=from_date, enddate=to_date, _type='daily') or {}
        else:
            race_predictions = {}

        # Convert race_predictions to an array if it's a dict
        if isinstance(race_predictions, dict):
            race_predictions = list(race_predictions.values())
        elif not isinstance(race_predictions, list):
            race_predictions = [race_predictions]

        # Combine the data into a single JSON object
        combined_data = {
            "activities": activities_with_splits,
            "race_predictions": race_predictions,
        }

        print(json.dumps(combined_data, indent=2))

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
