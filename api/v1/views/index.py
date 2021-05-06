#!/usr/bin/python3
""" Your first endpoint (route) will be to return the status of your API """
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app_views.route('/status')
def status_ok():
    """ prints json rep. status: ok """
    return jsonify(status='OK')

@app_views.route('/stats')
def class_counter():
    """ Endpoint that retrieves the number of each objects by type """
    amenities = storage.count(Amenity)
    cities = storage.count(City)
    places = storage.count(Place)
    reviews = storage.count(Review)
    states = storage.count(State)
    users = storage.count(User)
    return jsonify(amenities=amenities, 
                   cities=cities, 
                   places=places, 
                   reviews=reviews, 
                   states=states, 
                   users=users)
