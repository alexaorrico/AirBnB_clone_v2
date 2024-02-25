#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ Get all states id
    """
    r = requests.get("http://0.0.0.0:5000/api/v1/states")
    r_j = r.json()

    state_ids = []
    for state_j in r_j:
        state_ids.append(state_j.get('id'))

    # Arizona + California

    """ POST /api/v1/places_search
    """
    r = requests.post("http://0.0.0.0:5000/api/v1/places_search", data=json.dumps(
        {'states': state_ids}), headers={'Content-Type': "application/json"})
    r_j = r.json()
    print(len(r_j))
