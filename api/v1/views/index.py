#!/usr/bin/python3
"""App views and route defined"""
from api.v1.views import app_views
from flask import Flask, request, jsonify
from models import storage


@app.route('/status', methods=['GET'])
def status():
    """Show the status"""
    if request.method == 'GET':
        response = {"status": "OK"}
        return jsonify(response)


@app.route('/api/v1/stats',  methods=['GET'])
def stats():
    """Implements the new count() function"""
    if request.method == 'GET':
        response = {}
        ALL_OBJ = {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
        }
        for key, value in ALL_OBJ.items():
            response[value] = storage.count(key)
        return jsonify(response)