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
        rs = requests.get("http://0.0.0.0:5000/api/v1/states/{}/cities".format(state_j.get('id')))
        rs_j = rs.json()
        if len(rs_j) != 0:
            state_id = state_j.get('id')
            break
    
    if state_id is None:
        print("State with cities not found")
    
    """ get city
    """
    r = requests.get("http://0.0.0.0:5000/api/v1/states/{}/cities".format(state_id))
    r_j = r.json()
    city_id = None
    for city_j in r_j:
        rc = requests.get("http://0.0.0.0:5000/api/v1/cities/{}/places".format(city_j.get('id')))
        rc_j = rc.json()
        if len(rc_j) != 0:
            city_id = city_j.get('id')
            break
    
    if city_id is None:
        print("City without cities not found")

    """ Get user
    """
    r = requests.get("http://0.0.0.0:5000/api/v1/users")
    r_j = r.json()
    user_id = r_j[0].get('id')

    
    """ POST /api/v1/cities/<city_id>/places
    """
    r = requests.post("http://0.0.0.0:5000/api/v1/cities/{}/places/".format(city_id), data=json.dumps({ 'user_id': user_id, 'name': "NewPlace", 'number_rooms': 4, 'number_bathrooms': 3, 'max_guest': 6, 'price_by_night': 100, 'latitude': 1.3, 'longitude': 2.3 }), headers={ 'Content-Type': "application/json" })
    print(r.status_code)
    r_j = r.json()
    print(r_j.get('id') is None)
    print(r_j.get('user_id') == user_id)
    print(r_j.get('name') == "NewPlace")
    