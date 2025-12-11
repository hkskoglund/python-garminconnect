#!/bin/sh
get_last_activity="$(~/github/python-garminconnect/demo.py get_last_activity)"
get_activity_splits="$(~/github/python-garminconnect/demo.py get_activity_splits)"
get_race_predictions="$(~/github/python-garminconnect/demo.py get_race_predictions)"
jq -n \
  --argjson last_activity "$get_last_activity" \
  --argjson activity_splits "$get_activity_splits" \
  --argjson race_predictions "$get_race_predictions" \
  '{ 
      last_activity: $last_activity,
      activity_splits: $activity_splits,
      race_predictions: $race_predictions
  }'

