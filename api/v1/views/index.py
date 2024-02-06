#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, Blueprint, render_template, abort
from models import storage


@app_views.route('/status', method='GET')
def status():
    """Return Status"""
    return (jsonify({"status": "OK"}))


@app_views.route('stats', method='GET')
def stats():
    return (jsonify({"amenities": storage.count(Amenity),
                     "cities": storage.count(City),
                     "places": storage.count(Place),
                     "reviews": storage.count(Review),
                     "states": storage.count(State),
                     "users": storage.count(User)}))
