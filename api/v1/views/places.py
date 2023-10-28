#!/usr/bin/python3
"""Contains all REST actions for city Objects"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models.place import Place
from models import storage
from models.state import State
from models.city import City
from models.user import User


@app_views.route('cities/<city_id>/places', methods=['GET'])
def all_city_places(city_id):
    """get all places in the city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    return jsonify([val.to_dict() for val in places])


@app_views.route('places/<place_id>', methods=['GET'])
def place_by_id(place_id):
    """get place by thier id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('places/<place_id>', methods=['DELETE'])
def del_place(place_id):
    """delete a place by thier id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('cities/<city_id>/places', methods=['POST'])
def place_by_id(city_id):
    """create a place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort make_response(jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    if 'user_id' not in data:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'name' not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    user = storage.get(User, data['user_id'])
    if user in None:
        abort(404)
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'])
def place_by_id(place_id):
    """update the place info"""
    palce = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort make_response(jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    if 'name' in request.json:
        place.name = data['name']
    place.save()
    return jsonify(place.to_dict())
