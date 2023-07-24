#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ Get one state
    """
    r = requests.get("http://0.0.0.0:5000/api/v1/states")
    r_j = r.json()
    state_id = r_j[0].get('id')

    """ PUT /api/v1/states/<state_id>
    """
    r = requests.put("http://0.0.0.0:5000/api/v1/states/{}".format(state_id), data={ 'name': "NewStateName" }, headers={ 'Content-Type': "application/x-www-form-urlencoded" })
    print(r.status_code)
