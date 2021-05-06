#!/usr/bin/python3
""" Your first endpoint (route) will be to return the status of your API """
from api.v1.views import app_views
from flask import jsonify
import models

@app_views.route('/status')
def status_ok():
    """ prints json rep. status: ok """
    return jsonify(status='OK')

@app_views.route('/stats')
def class_counter():
    """ Endpoint that retrieves the number of each objects by type """
    amenities = models.storage.count("Amenity")
    cities = models.storage.count("City")
    places = models.storage.count("Place")
    reviews = models.storage.count("Review")
    states = models.storage.count("State")
    users = models.storage.count("User")
    return jsonify(amenities=amenities, 
                   cities=cities, 
                   places=places, 
                   reviews=reviews, 
                   states=states, 
                   users=users)
