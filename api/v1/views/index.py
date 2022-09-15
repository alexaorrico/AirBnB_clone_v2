#!/usr/bin/python3
"""return json object"""


from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status():
    """Return json with status"""
    ret = {"status": "OK"}
    return jsonify(ret)

@app_views.route('/stats')
def stats():
    """retrieves the number of eack objects by type"""
    new_dict = dict()
    new_dict['amenities'] = storage.count('Amenity')
    new_dict['cities'] = storage.count('City')
    new_dict['places'] = storage.count('Place')
    new_dict['review'] = storage.count('Review')
    new_dict['states'] = storage.count('State')
    new_dict['users'] = storage.count('User')
    return jsonify(new_dict)

