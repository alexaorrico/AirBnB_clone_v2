#!/usr/bin/python3
""" Create a new view for Place objects that handles all
    default RESTFul API actions
"""

from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, abort, request
from models.user import User
from models.city import City
from models.place import Place
from models.__init__ import storage


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def place_abor(city_id=None):
    """ Retrieves the list of all city.places objects """
    city = storage.get("City", city_id)
    lista = []
    if city is None:
        abort(404)
    else:
        for value in city.places:
            lista.append(value.to_dict())
        return jsonify(lista)


@app_views.route("/places/<place_id>", methods=['GET'],
                 strict_slashes=False)
def place_abor2(place_id=None):
    """ Retrieves the list of all places objects """
    place = storage.get("Place", place_id)
    lista = []
    if place is None:
        abort(404)
    else:
        return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def place_del(place_id=None):
    """delete a object if it is into places """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id=None):
    """ post method place, You must use request.get_json from Flask """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Not a JSON'}), 400
    if "user_id" not in json_data.keys():
        return jsonify({'error': "Missing user_id"}), 400
    if "name" not in json_data.keys():
        return jsonify({'error': "Missing name"}), 400
    user = storage.get("User", json_data['user_id'])
    if user is None:
        abort(404)
    json_data['city_id'] = city_id
    place = Place(**json_data)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id=None):
    """ method put Updates a Place object: PUT """
    p_place = storage.get("Place", place_id)
    if p_place is None:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in json_data.items():
        if key != "__class__":
            setattr(p_place, key, value)
    storage.save()
    return jsonify(p_place.to_dict()), 200
