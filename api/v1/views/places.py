#!/usr/bin/python3
"""view for places objects"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def all_places(city_id):
    """Retrieves the list of all places given an City"""
    places_list = []
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    for place in city.places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', strict_slashes=False)
def place_by_id(place_id):
    """Retrieves a place by a given ID"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
    '/places/<place_id>',
    methods=['DELETE'],
    strict_slashes=False
    )
def delete_place(place_id):
    """Deletes a place object"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/cities/<city_id>/places',
    methods=['POST'],
    strict_slashes=False
    )
def create_place(city_id):
    """Creates a place object"""
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request_data:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get('User', request_data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in request_data:
        return jsonify({"error": "Missing name"}), 400
    request_data['city_id'] = city_id
    obj = Place(**request_data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update a place object"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "Not a JSON"}), 400
    for k, v in request_data.items():
        setattr(place, k, v)
    storage.save()
    return jsonify(place.to_dict()), 200
