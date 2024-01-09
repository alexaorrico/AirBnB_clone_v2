#!/usr/bin/python3
"""
Flask route definitions for API status and statistics.
"""

# Importing necessary modules and packages
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Endpoint to check the API status.

    Returns:
        JSON object: A JSON response indicating the status as "OK".
    """
    if request.method == 'GET':
        response = {"status": "OK"}
        return jsonify(response)

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """
    Endpoint to retrieve counts of various class objects.

    Iterates through predefined classes and fetches their respective counts using the storage engine.

    Returns:
        JSON object: A JSON response containing counts of Amenity, City, Place, Review, State, and User objects.
    """
    if request.method == 'GET':
        response = {}
        # Dictionary mapping singular class names to their respective plural form for endpoint
        PLURALS = {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
        }
        # Iterate through classes, count objects, and populate the response dictionary
        for singular, plural in PLURALS.items():
            response[plural] = storage.count(eval(singular))
        return jsonify(response)
