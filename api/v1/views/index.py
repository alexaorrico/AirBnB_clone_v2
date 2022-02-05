#!/usr/bin/python3
"""Creationg route for Blueprint
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/status')
def response():
    """ get status ok
    """
    dic = {"status": "OK"}
    return jsonify(dic)


@app_views.route('/stats')
def class_counter():
    """ get a dictionary from count method
    """
    dic = {}
    dic["amenities"] = storage.count("Amenity")
    dic["cities"] = storage.count("City")
    dic["places"] = storage.count("Place")
    dic["reviews"] = storage.count("Review")
    dic["states"] = storage.count("State")
    dic["users"] = storage.count("User")
    return jsonify(dic)