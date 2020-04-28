#!/usr/bin/python3

from api.v1.views import app_views
from models import storage

@app_views.route('/status')
def status():
    return ({"status": "OK"})

@app_views.route('/stats')
def stats():
    classes = {"users": 'User', "states": 'State', "amenities": 'Amenity',
            "cities": 'City', "places": 'Place', "reviews": 'Review'}
    json = {}
    for key, value in classes.items():
        json[key] = storage.count(value)
    return json
    
