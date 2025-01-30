#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ POST /api/v1/states/
    """
    r = requests.post("http://0.0.0.0:5000/api/v1/states/", data=json.dumps({ 'name': "NewState" }), headers={ 'Content-Type': "application/json" })
    print(r.status_code)
    r_j = r.json()
    print(r_j.get('id') is None)
    print(r_j.get('name') == "NewState")