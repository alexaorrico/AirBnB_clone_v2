#!/usr/bin/python3
'''Defines the JSON GET request from the application'''
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from api.v1.views import app_views
from models import storage
from flask import jsonify, request


@app_views.route('/status')
def status():
    '''Returns json response as the status'''
    status = {
        "status": "OK"
    }
    return jsonify(status)


@app_views.route('/stats', methods=['GET'])
def stats():
    '''Returns the count of all class objects'''
    if request.method == 'GET':
        response = {}
        PLURALS = {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
        }
        for key, value in PLURALS.items():
            response[value] = storage.count(key)
        return jsonify(response)
