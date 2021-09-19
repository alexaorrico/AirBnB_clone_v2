#!/usr/bin/python3
"""
index for App views of AirBnB_clone
"""

from flask import jsonify
from models import storage
from api.v1.views import app_views

@app_views.route('/status')
def status():
    ''' returns a JSON: "status": "OK" '''
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def count():
    ''' retrieves the number of each objects by type: '''
    objcount = {}
    classes = {"Amenity": "amenities",
               "City": "cities",
               "Place": "places",
               "Review": "reviews",
               "State": "states",
               "User": "users"}
    for cls in classes:
        count = storage.count(cls)
        objcount[classes.get(cls)] = count
    return jsonify(objcount)
