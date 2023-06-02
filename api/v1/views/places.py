#!/usr/bin/python3
"""
Module for view for Place objects
It handles all default RESTful API actions
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User
from models.place import Place
from models.city import City


@app_views.route('/cities/<string:city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places_list(city_id):
    """
    Retrieves the list of all Place objects
    Based on the city

    Args:
        city_id - The id of the City object

    Returns:
        404: if city_id supplied is not linked to any state object
        List of all Place objects
    """
    places_list = []
    city = storage.get(City, city_id)
    if not city:
        return jsonify({"error": "Not found"}), 404
    for place in city.places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<string:place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a Place object

    Args:
        place_id: The id of the place object

    Returns:
        Place Object dictionary or 404
    """
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<string:city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place object"""
    city = storage.get(City, city_id)
    if not city:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    if "user_id" not in data:
        return jsonify({"error", "Missing user_id"}), 400
    user = storage.get(User, data["user_id"])
    if not user:
        return jsonify({"error": "Not found"}), 404
    if 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400
    data['city_id'] = city_id
    place = Place(**data)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<string:place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not found"}), 404
    ignored_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict())
