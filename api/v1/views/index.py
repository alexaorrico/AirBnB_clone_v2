#!/usr/bin/python3
'''module for storing blueprint routes'''
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.amenity import Amenity
from models.review import Review
from models.place import Place
from models.state import State
from models.city import City
from models.user import User

@app_views.route('/status')
def return_status():
    '''returns status'''
    status = {'status': 'OK'}
    return(jsonify(status))

@app_views.route("/status")
def return_status():
    '''returns api status'''
    return({"status": "OK"})

@app_views.route("/stats")
def return_stats():
    '''returns count of objs available of each type'''
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    stats = {}

    for key, obj in classes.items():
        stats[key] = storage.count(obj)

    return(jsonify(stats))
