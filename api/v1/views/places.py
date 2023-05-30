#!/usr/bin/python3
"""
Module for view for Place objects
It handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.place import Place


@app_views.route('/places', methods=['GET'], strict_slashes=False)
def get_places_list():
    """Retrieves the list of all Place objects"""
    places_list = []
    places = storage.all(Place).values()
    for place in places:
        places_list.append(place.to_dict())
    return jsonify(places_list), 200


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_places_obj(place_id):
    """
    Retrieves a Place object

    Args:
        place_id: The id of the place object
    Raises:
        404: if place_id supplied is not linked to any place object
    """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict()), 200
    else:
        return jsonify({"error": "Not found"}), 404


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_places_obj(place_id):
    """
    Deletes a Place object

    Args:
        place_id: The id of the place object
    Raises:
        404: if place_id supplied is not linked to any place object
    """
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/', methods=['POST'], strict_slashes=False)
def post_place():
    """
    Creates a Place object

    Returns:
        The new Place with the status code 201
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place object

    Args:
        place_id: The id of the Place object
    Raises:
        404:
            If place_id supplied is not linked to any Place object
            400: If the HTTP body request is not valid JSON
    """
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({'error': 'Not found'}), 404
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    data.pop('id', None)
    data.pop('created_at', None)
    data.pop('updated_at', None)
    for key, value in data.items():
        setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
