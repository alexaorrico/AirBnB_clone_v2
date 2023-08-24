#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ get the state with cities
    """
    r = requests.get("http://0.0.0.0:5000/api/v1/states")
    r_j = r.json()

    state_id = None
    for state_j in r_j:
        rs = requests.get(
            "http://0.0.0.0:5000/api/v1/states/{}/cities".format(state_j.get('id')))
        rs_j = rs.json()
        if len(rs_j) != 0:
            state_id = state_j.get('id')
            break

    if state_id is None:
        print("State with cities not found")

    """ Fetch cities
    """
    r = requests.get(
        "http://0.0.0.0:5000/api/v1/states/{}/cities".format(state_id))
    r_j = r.json()
    city_id = r_j[0].get('id')

    """ GET /api/v1/cities/<city_id>
    """
    r = requests.get("http://0.0.0.0:5000/api/v1/cities/{}".format(city_id))
    print(r.status_code)
    r_j = r.json()
    print(r_j.get('id') == city_id)
    print(r_j.get('name') is None)
