#!/usr/bin/python3
"""place view"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places():
    """Retrieves the list of of all Place objects"""
    places = storage.all(Place).values()
    return jsonify([place.to_dict() for place in places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(id):
    """Retrieves a Place object"""
    place = storage.get(Place, id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place():
    """Creates a Place"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200
