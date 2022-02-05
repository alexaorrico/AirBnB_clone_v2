#!/usr/bin/python3
'''
Import Blueprint to create routes
'''
from api.v1.views import app_views
from flask import Response
import json
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def status():
    '''Function to route status, return a json'''
    m = {
        'status': 'OK'
    }
    return Response(json.dumps(m), mimetype='application/json')


@app_views.route('/stats')
def stats():
    '''Function to route stats, return a json'''
    classes = {"amenities": Amenity,
               "cities": City,
               "places": Place,
               "reviews": Review, "states": State, "users": User}
    m = {}
    for k, v in classes.items():
        m[k] = storage.count(v)
    return Response(json.dumps(m), mimetype='application/json')
