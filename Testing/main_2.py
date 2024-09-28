#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ Get one amenity
    """
    r = requests.get("http://0.0.0.0:5050/api/v1/amenities")
    r_j = r.json()
    amenity_id = r_j[0].get('id')

    """ GET /api/v1/amenities/<amenity_id>
    """
    r = requests.get("http://0.0.0.0:5050/api/v1/amenities/{}".format(amenity_id))
    print(r.status_code)
    r_j = r.json()
    print(r_j.get('id') == amenity_id)
    print(r_j.get('name') is None)
