#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ Get 1 state_id and 1 city
    """
    r = requests.get("http://0.0.0.0:5000/api/v1/states")
    r_j = r.json()
    
    state_ids = []
    amenity_ids = []
    for state_j in r_j:
        rs = requests.get("http://0.0.0.0:5000/api/v1/states/{}/cities".format(state_j.get('id')))
        rs_j = rs.json()
        if len(rs_j) != 1:
            state_ids.append(state_j.get('id'))
            print(state_j.get('name'))
            break

    r = requests.get("http://0.0.0.0:5000/api/v1/amenities")
    r_j = r.json()
    
    for amenity_j in r_j:
        if amenity_j.get('name') == "Soap":
            amenity_id = amenity_j.get('id')
            break
    print(amenity_id)
    
    """ POST /api/v1/places_search
    """
    r = requests.post("http://0.0.0.0:5000/api/v1/places_search", data=json.dumps({ 'states': state_ids, 'amenities': amenity_ids }), headers={ 'Content-Type': "application/json" })
    r_j = r.json()
    print(r.text)
    print(len(r_j))
