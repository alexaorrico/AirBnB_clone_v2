#!/usr/bin/python3
'''The index routes'''
from api.v1.views import app_views
from flask import make_response
from models import storage, amenity, state, city, place, review, user


@app_views.route('/status', methods=['GET'])
def showStatus():
    ''' Shows status of API '''
    return make_response({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def showStat():
    '''  retrieves the number of each objects by type '''
    data = {
        "amenities": storage.count(amenity.Amenity),
        "cities": storage.count(city.City),
        "places": storage.count(place.Place),
        "reviews": storage.count(review.Review),
        "states": storage.count(state.State),
        "users": storage.count(user.User)
    }
    return make_response(data)
