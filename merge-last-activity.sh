#!/bin/sh
get_last_activity="$(~/github/python-garminconnect/demo.py get_last_activity)"
get_activity_splits="$(~/github/python-garminconnect/demo.py get_activity_splits)"
jq -n \
  --argjson last_activity "$get_last_activity" \
  --argjson activity_splits "$get_activity_splits" \
  '$last_activity * $activity_splits'
