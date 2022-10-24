#!/usr/bin/python3
"""
module to generate json response
"""

from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def all_cities(state_id):
    """ display all cities """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    response = []
    cities = state.cities
    for city in cities:
        response.append(city.to_dict())
    return jsonify(response)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def city_by_id(city_id=None):
    """ display city by id """
    response = storage.get(City, city_id)
    if response is None:
        abort(404)
    return jsonify(response.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def del_city(city_id=None):
    """ delete city by id """
    if city_id is None:
        abort(404)
    else:
        trash = storage.get(City, city_id)
        if trash is not None:
            storage.delete(trash)
            storage.save()
            return make_response(jsonify({}), 200)
        else:
            abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ create new city to a specific state """
    if state_id is None:
        abort(404)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    body = request.get_json()
    if body is None:
        abort(400, 'Not a JSON')
    if 'name' not in body.keys():
        abort(400, 'Missing name')
    body['state_id'] = state.id
    obj = City(**body)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id=None):
    """ update an existing city """
    response = storage.get(City, city_id)
    if city_id is None or response is None:
        abort(404)
    try:
        new = request.get_json()
    except Exception:
        pass
    if new is None or type(new) is not dict:
        abort(400, 'Not a JSON')
    for key in new.keys():
        if key != 'id' and key != 'created_at' and\
           key != 'state_id' and key != 'updated_at':
            setattr(response, key, new[key])
    response.save()
    return make_response(jsonify(response.to_dict()), 200)
