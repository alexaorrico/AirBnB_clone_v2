#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ POST /api/v1/amenities
    """
    r = requests.post("http://0.0.0.0:5050/api/v1/amenities/", data=json.dumps({ 'fake_name': "Fridge" }), headers={ 'Content-Type': "application/json" })
    print(r.status_code)
