#!/usr/bin/python3
"""Module to create a new view for Place objects"""

from flask import jsonify, Flask, request
from models import storage
from api.v1.views import app_views
from models.state import State
from models.city import City
from models.place import Place

@app_views.route('cities/<city_id>/places', methods=['GET'],
                 strict_slashes = False)
def get_places(city_id):
    """Retrieves the list of all Place objects by city_id"""
    place = storage.get('Place', str(place_id))
    if city is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(place.to_dict())

@app_views.route('places/<place_id>', methods=['GET'],
                 strict_slashes = False)
def get_place_by_place_id(place_id):
    """Retrieves a Place objects by place_id"""
    place = storage.get('Place', str(place_id))
    if place is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(place.to_dict())

@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes = False)
def delete_place_by_id(place_id):
    """Deletes a place by ID"""
    place = storage.get('Place', str(place_id))
    if place is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(place)
    storage.save()
    return jsonify({}), 200

@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes = False)
def create_place(place_id):
    """Post a Place object"""
    data = request.get_json()
    if not data:
        abort(400)
        abort(Response("Not a JSON"))
    if 'name' not in data:
        abort(400)
        abort(Response("Missing name"))
    new_place = Place(**data)
    return jsonify(new_place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes = False)
def put_place(place_id):
    """Put a Place object"""
    data = request.get_json()
    if not data:
        abort(400)
        abort(Response("Not a JSON"))
    new_place = Place(**data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 200
