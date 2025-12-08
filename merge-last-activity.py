#!/usr/bin/env python3
"""
Merges the data from 'get_last_activity' and 'get_activity_splits' using the Garmin API.

This script directly uses the python-garminconnect library to fetch the last
activity and its corresponding splits. It then merges the two data structures
and prints the combined JSON to stdout.

It reuses the API initialization logic from demo.py to handle authentication.
"""

import json
import sys

# Import the API initialization function and configuration from demo.py
# This allows us to reuse the robust authentication and token handling.
from demo import init_api


def deep_merge(source: dict, destination: dict) -> dict:
    """
    Recursively merges the `source` dictionary into the `destination` dictionary.

    If a key exists in both, the value from `source` is used. For nested
    dictionaries, a recursive merge is performed.

    Args:
        source: The dictionary to merge from.
        destination: The dictionary to merge into.

    Returns:
        The merged dictionary.
    """
    for key, value in source.items():
        if isinstance(value, dict) and key in destination and isinstance(destination[key], dict):
            destination[key] = deep_merge(value, destination[key])
        else:
            destination[key] = value
    return destination


def main():
    """
    Main function to execute demo.py, capture, and merge JSON outputs.
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
        last_activity = api.get_last_activity()

        if not last_activity:
            print("No last activity found.", file=sys.stderr)
            sys.exit(0)

        activity_id = last_activity.get("activityId")
        if not activity_id:
            print("Could not determine activityId from last activity.", file=sys.stderr)
            sys.exit(1)

        print(f"Fetching splits for activity ID: {activity_id}", file=sys.stderr)
        activity_splits = api.get_activity_splits(activity_id)

        merged_data = deep_merge(activity_splits or {}, last_activity)

        print(json.dumps(merged_data, indent=2))

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
