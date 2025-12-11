#!/usr/bin/env python3
"""
Fetches and combines data from 'get_last_activity', 'get_activity_splits',
and 'get_race_predictions' using the Garmin API.

This script directly uses the python-garminconnect library to fetch the last
activity, its splits, and race predictions. It then combines them into a
single JSON object and prints it to stdout.

It reuses the API initialization logic from demo.py to handle authentication.
"""

import json
import sys

# Import the API initialization function and configuration from demo.py
# This allows us to reuse the robust authentication and token handling.
from demo import init_api


def main():
    """
    Main function to fetch and combine Garmin Connect data.
    """
    # Initialize the Garmin API. This will handle login, token refresh, and MFA.
    # We pass credentials as None to use environment variables or prompt the user.
    print("Initializing Garmin Connect API...", file=sys.stderr)
    api = init_api(email=None, password=None)

    if not api:
        print("API initialization failed. Exiting.", file=sys.stderr)
        sys.exit(1)

    try:
        print("Fetching last activity...", file=sys.stderr)
        last_activity = api.get_last_activity() or {}

        activity_id = last_activity.get("activityId")
        activity_splits = {}
        if activity_id:
            print(f"Fetching splits for activity ID: {activity_id}", file=sys.stderr)
            activity_splits = api.get_activity_splits(activity_id) or {}
        else:
            print("No activityId found in last activity, skipping splits.", file=sys.stderr)

        print("Fetching race predictions...", file=sys.stderr)
        race_predictions = api.get_race_predictions() or {}

        # Combine the data into a single JSON object, similar to the shell script
        combined_data = {
            "last_activity": last_activity,
            "activity_splits": activity_splits,
            "race_predictions": race_predictions,
        }

        print(json.dumps(combined_data, indent=2))

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
