#!/usr/bin/python3
""" cretaing route """

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app.route('/status')
def status():
    """ return status ok """
    res = {"status": "OK"}
    return jsonify(res)


@app.route('/stats')
def stats():
    """ get stats """
    stat = {}
    stat["amenities"] = storage.count("Amenity")
    stat["cities"] = storage.count("CIty")
    stat["places"] = storage.count("Place")
    stat["reviews"] = storage.count("Review")
    stat["states"] = storage.count("State")
    stat["users"] = storage.count("User")
    return jsonify(stat)
