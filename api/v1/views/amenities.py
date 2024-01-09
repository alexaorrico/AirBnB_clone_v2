#!/usr/bin/python3
"""holds class Amenity
"""
from flask import Blueprint, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


# Define route for amenities handling GET and POST requests
@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def get_post_amenities():
    """Handles GET (retrieve all amenities) and
    POST (create new amenity) requests"""
    if request.method == 'GET':
        all_amenities = [
                amenity.to_dict()
                for amenity in storage.all('Amenity').values()
                ]
        return jsonify(all_amenities)
    elif request.method == 'POST':
        # Create a new amenity based on POST data in JSON format
        request_data = request.get_json()
        if request_data is None or not isinstance(request_data, dict):
            return jsonify({'error': 'Invalid JSON'}), 400
        elif 'name' not in request_data:
            return jsonify({'error': 'Missing name parameter'}), 400
        new_amenity = Amenity(**request_data)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


# Endpoint to handle GET, PUT, and DELETE requests
@app_views.route(
        '/amenities/<string:amenity_id>',
        methods=['GET', 'PUT', 'DELETE'],
        strict_slashes=False
        )
def get_put_delete_amenity(amenity_id):
    """Handles GET (retrieve), PUT (update), and DELETE (remove)"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)  # Return 404 if amenity with given ID doesn't exist
    elif request.method == 'GET':
        # Return details of the amenity in JSON format
        return jsonify(amenity.to_dict())
    elif request.method == 'DELETE':
        storage.delete(amenity)  # Delete the specified amenity
        storage.save()  # Save changes
        return jsonify({}), 200

    elif request.method == 'PUT':
        # Update attributes of the amenity based on PUT
        put_data = request.get_json()
        if put_data is None or not isinstance(put_data, dict):
            return jsonify({'error': 'Invalid JSON'}), 400
        for key, value in put_data.items():
            if key not in ('id', 'created_at', 'updated_at'):
                setattr(amenity, key, value)
        storage.save()  # Save changes
        return jsonify(amenity.to_dict()), 200
