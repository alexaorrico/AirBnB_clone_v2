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

    """ PUT /api/v1/amenities/<amenity_id>
    """
    r = requests.put("http://0.0.0.0:5050/api/v1/amenities/{}".format(amenity_id), data={ 'name': "NewAmenityName" }, headers={ 'Content-Type': "application/x-www-form-urlencoded" })
    print(r.status_code)
