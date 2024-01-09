#!/usr/bin/python3
""" holds class Place"""

from flask import Blueprint, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route(
        '/cities/<string:city_id>/places',
        methods=['GET', 'POST'],
        strict_slashes=False
        )
def get_post_places(city_id):
    """Handles GET and POST requests"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)  # Return 404 if city with given ID doesn't exist
    if request.method == 'GET':
        # Retrieve all places in the city and return in JSON format
        return jsonify([place.to_dict() for place in city.places])
    elif request.method == 'POST':
        # Create a new place in the city based on POST data in JSON format
        request_data = request.get_json()
        if request_data is None or not isinstance(request_data, dict):
            return jsonify({'error': 'Invalid JSON'}), 400
        elif 'name' not in request_data or 'user_id' not in request_data:
            return jsonify({
                'error': 'Missing name or user_id parameters'
                }), 400
        elif storage.get('User', request_data['user_id']) is None:
            abort(404)  # Return 404 if user with given ID doesn't exist
        new_place = Place(city_id=city_id, **request_data)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route(
        '/places/<string:place_id>',
        methods=['GET', 'PUT', 'DELETE'],
        strict_slashes=False
        )
def get_put_delete_place(place_id):
    """Handles GET (retrieve), PUT (update), and DELETE (remove)"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)  # Return 404 if place with given ID doesn't exist
    elif request.method == 'GET':
        # Return details of the place in JSON format
        return jsonify(place.to_dict())
    elif request.method == 'DELETE':
        storage.delete(place)  # Delete the specified place
        storage.save()  # Save changes
        return jsonify({}), 200
    elif request.method == 'PUT':
        # Update attributes of the place based PUT
        put_data = request.get_json()
        if put_data is None or not isinstance(put_data, dict):
            return jsonify({'error': 'Invalid JSON'}), 400
        for key, value in put_data.items():
            if key != 'id' and \
                    key != 'created_at' and \
                    key != 'updated_at' and \
                    key != 'city_id' and \
                    key != 'user_id':
                setattr(place, key, value)
        storage.save()  # Save changes
        return jsonify(place.to_dict()), 200  # Return update
