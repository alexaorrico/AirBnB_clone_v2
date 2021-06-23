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
    obj_dict = {}
    obj_dict['amenities'] = storage.count(Amenity)
    obj_dict['states'] = storage.count(State)
    obj_dict['cities'] = storage.count(City)
    obj_dict['places'] = storage.count(Place)
    obj_dict['reviews'] = storage.count(Review)
    obj_dict['users'] = storage.count(User)
    return jsonify(obj_dict)
