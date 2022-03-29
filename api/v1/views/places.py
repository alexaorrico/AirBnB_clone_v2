#!/usr/bin/python3
""" API view for Place objects. """
from api.v1.views import app_views
from flask import jsonify, request, abort
import json
from models import storage
from models.city import City
from models.place import Place
from models.user import User

import os


@app_views.route('\
/cities/<city_id>/places', strict_slashes=False, methods=['GET'])
def all_places(city_id):
    """ Returns the list of places in City obj in JSON. """
    place_list = []
    try:
        city = storage.all(City)["City.{}".format(city_id)]
    except (TypeError, KeyError):
        abort(404)
    if not city:
        abort(404)
    all_places = storage.all(Place)
    for place in all_places.values():
        if place.city_id == city_id:
            place_list.append(place.to_dict())
    return jsonify(place_list)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def get_place(place_id):
    """ Returns the Place obj in JSON. """
    try:
        place = storage.all(Place)["Place.{}".format(place_id)]
    except (TypeError, KeyError):
        abort(404)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('\
/places/<place_id>', strict_slashes=False, methods=['DELETE'])
def delete_place(place_id):
    """ Deletes the Place obj from Storage. """
    try:
        place = storage.all(Place)["Place.{}".format(place_id)]
    except (TypeError, KeyError):
        abort(404)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('\
/cities/<city_id>/places', strict_slashes=False, methods=['POST'])
def create_place(city_id):
    """ Creates a Place obj and saves to Storage. """
    try:
        city = storage.all(City)["City.{}".format(city_id)]
    except (TypeError, KeyError):
        abort(404)
    if not city:
        abort(404)
    content = request.get_json()
    try:
        json.dumps(content)
        if 'name' not in request.json:
            abort(400, {'message': 'Missing name'})
        if 'user_id' not in content:
            abort(400, {'message': 'Missing user_id'})
    except (TypeError, OverflowError):
        abort(400, {'message': 'Not a JSON'})
    try:
        user = storage.all(User)["User.{}".format(content['user_id'])]
    except (TypeError, KeyError):
        abort(404)
    if not user:
        abort(404)
    content['city_id'] = city_id
    new_place = Place(**content)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """ Updates a Place obj to Storage. """
    if not request.json:
        abort(400, {'message': 'Not a JSON'})
    try:
        place = storage.all(Place)["Place.{}".format(place_id)]
    except (TypeError, KeyError):
        abort(404)
    if not place:
        abort(404)
    content = request.get_json()
    json.dumps(content)

    ignored_keys = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']
    for key, value in content.items():
        if key not in ignored_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
