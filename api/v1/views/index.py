#!/bin/usr/python3
"""Endpoint (route) that returns the status of the API"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from models import storage
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State

@app_views.route('/status')
def serialized_status():
    """Return status of the API jsonified"""
    return jsonify(status='OK')


@app_views.route('/stats')
def stats():
    CLSs = {User: "users",
                        Amenity: "amenities", City: "cities",
                        Place: "places", Review: "reviews",
                        State: "states"}
    stats = {}
    for value in CLSs.keys():
        stats[CLSs[value]] = storage.count(value)
    return jsonify(stats)
