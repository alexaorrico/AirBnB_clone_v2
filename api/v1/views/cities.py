#!/usr/bin/python
""" holds class City"""

from flask import Blueprint, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route(
        '/states/<string:state_id>/cities',
        methods=['GET', 'POST'],
        strict_slashes=False
        )
def get_post_cities(state_id):
    """Handles GET (retrieve all cities in a state) and POST"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)  # Return 404 if state with given ID doesn't exist
    if request.method == 'GET':
        # Retrieve all cities in the state and return in JSON format
        return jsonify([city.to_dict() for city in state.cities])
    elif request.method == 'POST':
        # Create a new city in the state based on POST data in JSON format
        request_data = request.get_json()
        if request_data is None or not isinstance(request_data, dict):
            return jsonify({'error': 'Invalid JSON'}), 400
        elif 'name' not in request_data:
            return jsonify({'error': 'Missing name parameter'}), 400
        new_city = City(state_id=state_id, **request_data)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route(
        '/cities/<string:city_id>',
        methods=['GET', 'PUT', 'DELETE'],
        strict_slashes=False
        )
def get_put_delete_city(city_id):
    city = storage.get('City', city_id)
    if city is None:
        abort(404)  # Return 404 if city with given ID doesn't exist
    elif request.method == 'GET':
        # Return details of the city in JSON format
        return jsonify(city.to_dict())
    elif request.method == 'DELETE':
        storage.delete(city)  # Delete the specified city
        storage.save()  # Save changes
        return jsonify({}), 200
    elif request.method == 'PUT':
        # Update attributes of the city based on PUT
        put_data = request.get_json()
        if put_data is None or not isinstance(put_data, dict):
            return jsonify({'error': 'Invalid JSON'}), 400
        for key, value in put_data.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(city, key, value)
        storage.save()  # Save changes
        return jsonify(city.to_dict()), 200
