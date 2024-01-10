#!/usr/bin/python3

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models import *

@app_views.route('/cities/<city_id>/places', methods=["GET"], strict_slashes=False)
def get_places(city_id):
    """get all places of city objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)

@app_views.route('places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """retrieve place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """method to delete place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200

@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False
def create_place(city_id):
    """creates new object place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if storage.get(User, data['user_id']) is None:
        abort(404)
    if 'name' not in data:
        abort(400, 'Missing name')
    place = Place(city_id=city_id, **data)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201

@app_views.route('places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """update place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for k, v in data.items():
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, k, v)
    city.save()
    return jsonify(place.to_dict()), 200
