#!/usr/bin/python3
"""A new view for places objects"""
from api.v1.views import app_views
from models import city, place, storage
from flask import Flask, jsonify, abort, request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places(city_id):
    """Retrieves the list of all Places"""
    get_city = storage.get('City', city_id)
    list_places = []
    if get_city is None:
        abort(404)
    for place in get_city.places:
        list_places.append(place.to_dict())
    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_id(place_id):
    """Retrieves a Place"""
    get_place = storage.get('Place', place_id)
    if get_place:
        return jsonify(get_place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def place_delete(place_id):
    """Deletes a Place"""
    get_place = storage.get('Place', place_id)
    if get_place:
        get_place.delete()
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def place_post(city_id):
    """Creates a Place"""
    get_city = storage.get('City', city_id)
    if get_city is None:
        abort(404)
    if not request.get_json():
        return jsonify({'message': 'Not a JSON'}), 400
    if "user_id" not in request.get_json():
        return jsonify({'message': 'Missing user_id'}), 400
    get_user = storage.get('User', request.get_json()['user_id'])
    if get_user is None:
        abort(404)
    if 'name' not in request.get_json():
        return jsonify({'message': 'Missing name'}), 400

    place = place.Place(request.get_json()['city_id'] = city_id)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def place_put(place_id):
    """Updates a Place"""
    get_place = storage.get('Place', place_id)
    if get_place is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')

    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
            setattr(get_place, k, v)
    get_place.save()
    return jsonify(get_place.to_dict())