#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ get the state with cities
    """
    r = requests.get("http://0.0.0.0:5050/api/v1/states")
    r_j = r.json()
    
    state_id = None
    for state_j in r_j:
        rs = requests.get("http://0.0.0.0:5050/api/v1/states/{}/cities".format(state_j.get('id')))
        rs_j = rs.json()
        if len(rs_j) != 0:
            state_id = state_j.get('id')
            break
    
    if state_id is None:
        print("State with cities not found")
    
    """ get city
    """
    r = requests.get("http://0.0.0.0:5050/api/v1/states/{}/cities".format(state_id))
    r_j = r.json()
    city_id = None
    for city_j in r_j:
        rc = requests.get("http://0.0.0.0:5050/api/v1/cities/{}/places".format(city_j.get('id')))
        rc_j = rc.json()
        if len(rc_j) != 0:
            city_id = city_j.get('id')
            break
    
    if city_id is None:
        print("City without places not found")
    
    """ get place with reviews
    """
    r = requests.get("http://0.0.0.0:5050/api/v1/cities/{}/places".format(city_id))
    r_j = r.json()
    place_id = None
    review_id = None
    for place_j in r_j:
        rp = requests.get("http://0.0.0.0:5050/api/v1/places/{}/reviews".format(place_j.get('id')))
        rp_j = rp.json()
        if len(rp_j) != 0:
            place_id = place_j.get('id')
            review_id = rp_j[0].get('id')
            break
    
    if place_id is None:
        print("Place with reviews not found")
    if review_id is None:
        print("Review not found")
    

    """ PUT /api/v1/reviews/<review_id>
    """
    r = requests.put("http://0.0.0.0:5050/api/v1/reviews/{}".format(review_id), data=json.dumps({ 'text': "NewTextReview" }), headers={ 'Content-Type': "application/json" })
    print(r.status_code)
    r_j = r.json()
    print(r_j.get('id') is None)
    print(r_j.get('text') == "NewTextReview")
    
    """ Fetch cities
    """
    r = requests.get("http://0.0.0.0:5050/api/v1/places/{}/reviews".format(place_id))
    r_j = r.json()
    for review_j in r_j:
        if review_j.get('id') == review_id:
            print(review_j.get('text') == "NewTextReview")