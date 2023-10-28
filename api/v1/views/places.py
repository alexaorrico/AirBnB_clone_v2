#!/usr/bin/python3
"""Contains all REST actions for place Objects"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models.place import Place
from models.user import User
from models import storage
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places(city_id):
    """retrieves a list of all place objects of city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    return jsonify([val.to_dict() for val in places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """retrieves a place objects"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """deletes a place objects"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def new_place(city_id):
    """creates a place objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in request.json:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    user = storage.get(User, request.json['user_id'])
    if user is None:
        abort(404)
    if 'name' not in request.json:
        return make_response(jsonify({"error": "Missing name"}), 400)
    data = request.get_json()
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """updates a place objects"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    data = {k: v for k, v in request.get_json().items()
            if k not in ['id', 'user_id', 'city_id', 'created_at',
            'updated_at']}
    for k, v in data.items():
        setattr(place, k, v)
    place.save()
    return jsonify(place.to_dict())
