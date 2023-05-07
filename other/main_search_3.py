#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ Get amenity_id with name Wifi
    """
    r = requests.get("http://0.0.0.0:5000/api/v1/amenities")
    r_j = r.json()
    
    amenity_id = None
    for amenity_j in r_j:
        if amenity_j.get('name') == "Wifi":
            amenity_id = amenity_j.get('id')
            break
                    
    """ POST /api/v1/places_search
    """
    r = requests.post("http://0.0.0.0:5000/api/v1/places_search", data=json.dumps({ 'amenities': [amenity_id] }), headers={ 'Content-Type': "application/json" })
    r_j = r.json()
    print(len(r_j))
