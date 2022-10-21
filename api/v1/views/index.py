#!/usr/bin/python3
"""
Flask routes and returns json status reponse
"""
from flask import Flask, jsonify, request
from api.v1.views import app_views
from models import storage

@app_views.route("/status", methods=["GET"])
def status():
    """Function for the status of the route"""
    if request.method == "GET":
        return jsonify({"status": "OK"})

@app_views.route("/stats", methods=["GET"])
def stats():
    """Function to count all objects of classes"""
    if request.method == 'GET':
        response = {}
        PLURALS = {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
        }
        for key, value in PLURALS.items():
            response[value] = storage.count(key)
        return jsonify(response)
