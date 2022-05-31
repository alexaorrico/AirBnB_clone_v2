#!/usr/bin/python3
""" Create a new view for City objects that handles all
    default RESTFul API actions
"""

import json
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, abort, request
from models.state import State
from models.city import City
from models import storage


@app_views.route("/states/<state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def state_abor(state_id=None):
    """ Retrieves the list of all state.cities objects """
    state = storage.get("State", state_id)
    lista = []
    if state is None:
        abort(404)
    else:
        for value in state.cities:
            lista.append(value.to_dict())
        return jsonify(lista)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def city_abor(city_id):
    """ Retrieves the list of all cities objects """
    city = storage.get("City", city_id)
    lista = []
    if city is None:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'],
                 strict_slashes=False)
def city_del(city_id=None):
    """delete a object if it is into states """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """ post method states, You must use request.get_json from Flask """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Not a JSON'}), 400
    if "name" not in json_data.keys():
        return jsonify({'error': "Missing name"}), 400
    json_data['state_id'] = state_id
    city = City(**json_data)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id=None):
    """ method put Updates a State object: PUT """
    p_city = storage.get("City", city_id)
    if p_city is None:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in json_data.items():
        if key != "__class__":
            setattr(p_city, key, value)
    storage.save()
    return jsonify(p_city.to_dict()), 200
