#!/usr/bin/python3
'''
    flask with general routes
    routes:
        /status:    display "status":"OK"
'''
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.place import Place
from models.user import User
from models.state import State


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    '''
        return JSON of OK status
    '''
    return jsonify({'status': 'OK'})

@app_views.route("/stats")
def stats():
    objs = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User) 
    }
    return jsonify(objs)
