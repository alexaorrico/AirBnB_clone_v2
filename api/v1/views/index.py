#!/usr/bin/python3
""" An endpoint that retrieves the number of objects by each type """
from api.v1.views import app_views
from flask import Flask, jsonify
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status')
def status():
    """ Return OK """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """ Using count() method from storage """
    Dict_of_obj = {}
    Dict_of_obj['amenities'] = storage.count(Amenity)
    Dict_of_obj['states'] = storage.count(State)
    Dict_of_obj['cities'] = storage.count(City)
    Dict_of_obj['places'] = storage.count(Place)
    Dict_of_obj['reviews'] = storage.count(Review)
    Dict_of_obj['users'] = storage.count(User)
    return jsonify(Dict_of_obj)
