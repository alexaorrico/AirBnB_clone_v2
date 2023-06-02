#!/usr/bin/python3
"""
Module that houses the view for City objects
It handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_city_list(state_id):
    """Retrieves the list of all City objects"""
    cities_list = []
    state = storage.get(State, state_id)
    if not state:
        return jsonify({"error": "Not found"}), 404
    for city in state.cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list), 200


@app_views.route('/cities/<city_id>',
                 methods=['GET'], strict_slashes=False)
def get_city_obj(city_id):
    """
    Retrieves an City object

    Args:
        city_id: The id of the city object
    Raises:
        404: if city_id supplied is not linked to any amenity object
    """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict()), 200
    else:
        return jsonify({"error": "Not found"}), 404


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_cities_obj(city_id):
    """
    Deletes an City object

    Args:
        city_id: The id of the city object
    Raises:
        404: if city_id supplied is not linked to any amenity object
    """
    city = storage.get(City, city_id)
    if not city:
        return jsonify({"error": "Not found"}), 404
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """
    Creates an City object

    Returns:
        The new City with the status code 201
    """
    state = storage.get(State, state_id)
    if not state:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400
    data["state_id"] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    Updates an City object

    Args:
        city_id: The id of the city object
    Raises:
        404:
            If city_id supplied is not linked to any city o    bject
            400: If the HTTP body request is not valid JSON
    """
    city = storage.get(City, city_id)
    if not city:
        return jsonify({'error': 'Not found'}), 404
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    data.pop('id', None)
    data.pop('state_id', None)
    data.pop('created_at', None)
    data.pop('updated_at', None)
    for key, value in data.items():
        setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
