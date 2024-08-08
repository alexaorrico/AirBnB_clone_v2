#!/usr/bin/python3
"""
Module defines view for Place objects that handles all default
RESTFUL API actions.
"""
from models import storage
from models.city import City
from models.place import Place
from flask import jsonify, abort, request
from werkzeug.exceptions import BadRequest
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_all_places(city_id):
    """ Retrieves the list of all Place objects of a city by city_id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place_list = [place.to_dict() for place in city.places]
    return jsonify(place_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieves Place object by place_id """
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    return jsonify(place_obj.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes Place object by place_id """
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    storage.delete(place_obj)
    storage.save()

    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """ Creates Place object in a city by city_id"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    try:
        data = request.get_json()
        if 'name' not in data:
            abort(400, description='Missing name')
    except BadRequest:
        abort(400, description='Not a JSON')

    data['city_id'] = city_id
    place_obj = Place(**data)
    storage.new(place_obj)
    storage.save()

    return jsonify(place_obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates Place object by place_id """
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    try:
        data = request.get_json()
    except BadRequest:
        abort(400, description='Not a JSON')

    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place_obj, key, value)

    storage.save()

    return jsonify(place_obj.to_dict()), 200
