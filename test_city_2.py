#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ Get one amenity
    """
    r = requests.get("http://0.0.0.0:5000/api/v1/amenities")
    r_j = r.json()
    amenity_id = r_j[0].get('id')

    """ PUT /api/v1/amenities/<amenity_id>
    """
    r = requests.put("http://0.0.0.0:5000/api/v1/amenities/{}".format(amenity_id),
                     data=json.dumps({'name': "NewAmenityName"}), headers={'Content-Type': "application/json"})
    print(r.status_code)
    r_j = r.json()
    print(r_j.get('id') == amenity_id)
    print(r_j.get('name') == "NewAmenityName")

    """ Verify if the state is updated
    """
    r = requests.get("http://0.0.0.0:5000/api/v1/amenities")
    r_j = r.json()
    for amenity_j in r_j:
        if amenity_j.get('id') == amenity_id:
            print(amenity_j.get('name') == "NewAmenityName")
