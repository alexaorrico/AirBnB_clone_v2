#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ POST /api/v1/amenities/
    """
    r = requests.post("http://0.0.0.0:5000/api/v1/amenities/", data=json.dumps(
        {'name': "Fridge"}), headers={'Content-Type': "application/json"})
    print(r.status_code)
    r_j = r.json()
    print(r_j.get('id') is None)
    print(r_j.get('name') == "Fridge")
