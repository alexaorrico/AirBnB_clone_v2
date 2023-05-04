#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ POST /api/v1/places_search
    """
    r = requests.post("http://0.0.0.0:5000/api/v1/places_search", data=json.dumps({}), headers={ 'Content-Type': "application/json" })
    r_j = r.json()
    print(type(r_j))
    print(len(r_j))
