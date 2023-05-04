#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ Get amenity_ids with name Wifi or Ethernet
    """
    r = requests.get("http://0.0.0.0:5000/api/v1/amenities")
    r_j = r.json()
    
    amenity_ids = []
    for amenity_j in r_j:
        if amenity_j.get('name') == "Wifi" or amenity_j.get('name') == "Ethernet":
            amenity_ids.append(amenity_j.get('id'))
                    
    """ POST /api/v1/places_search
    """
    r = requests.post("http://0.0.0.0:5000/api/v1/places_search", data=json.dumps({ 'amenities': amenity_ids }), headers={ 'Content-Type': "application/json" })
    r_j = r.json()
    print(r_j)
    print(len(r_j))
