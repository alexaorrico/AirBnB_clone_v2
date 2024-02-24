#!/usr/bin/python3
"""
This file contains the Place module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """ Gets places for city_id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [obj.to_dict() for obj in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """ get place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """ delete place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """ create new instance """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return (jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return (jsonify({"error": "Missing name"}), 400)
    if 'user_id' not in request.get_json():
        return (jsonify({"error": "Missing user_id"}), 400)
    user_id = request.get_json().get('user_id')
    if not storage.get(User, user_id):
        abort(404)

    place = Place(**request.get_json())
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/cities/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates the place method"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in request.get_json().items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
