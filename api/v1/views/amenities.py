#!/usr/bin/python3

""" View module for Amenity objects that handles all default
RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False,
                 methods=['GET', 'POST'])
def amenities():
    """Handles GET and POST requests for Amenity objects."""
    if request.method == 'GET':
        # Return a JSON representation of all Amenity objects
        return jsonify([amenity.to_dict()
                        for amenity in storage.all(Amenity).values()])

    elif request.method == 'POST':
        # Handle POST request to create a new Amenity object
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        if 'name' not in data:
            return jsonify({"error": "Missing name"}), 400

        # Create a new Amenity instance and save it
        new_amenity = Amenity(**data)
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def amenity_by_id(amenity_id):
    """Handles GET, DELETE, and PUT requests for a specific Amenity object."""
    # Retrieve the Amenity object with the given ID
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        # Return a 404 error if the Amenity object is not found
        abort(404)

    if request.method == 'GET':
        # Return a JSON representation of the specific Amenity object
        return jsonify(amenity.to_dict())

    elif request.method == 'DELETE':
        # Handle DELETE request to delete the specific Amenity object
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200

    elif request.method == 'PUT':
        # Handle PUT request to update the specific Amenity object
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a JSON"}), 400

        # Update the Amenity object's attributes based on the request data
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(amenity, key, value)
        # Save the updated Amenity object
        storage.save()
        return jsonify(amenity.to_dict()), 200
