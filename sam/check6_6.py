#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    r = requests.get("http://0.0.0.0:5000/api/v1/states")
    r_j = r.json()
    print(type(r_j))
    print(len(r_j))
    for state_j in r_j:
        if state_j.get('name') in ["California", "Arizona", "Nevada", "Louisiana"]:
            print("OK")
        else:
            print("Missing: {}".format(state_j.get('name')))
    if state_j.get('id') is None:
        print("Missing ID for State: {}".format(state_j.get('name')))