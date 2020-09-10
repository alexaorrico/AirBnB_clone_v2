#!/usr/bin/python3
"""cutty sark"""
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, abort, request, Blueprint


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """return list of all cities in state"""
    lizt = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for city in state.cities:
        lizt.append(city.to_dict())
    return jsonify(lizt)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_a_city(city_id):
    """retrieve of specific City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    ret = city.to_dict()
    return jsonify(ret)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def del_a_city(city_id):
    """delete a specific city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_a_city(state_id):
    """create a city"""
    req = request.get_json()
    if not request.is_json:
        abort(400, description="Not a JSON")
    state = storage.get(State, state_id)
    """verifying the state_id is for an actual state and not a junk id"""
    if state is None:
        abort(404)
    key = 'name'
    if key not in req:
        abort(400, description="Missing name")
    req['state_id'] = state_id
    new_city = City(**req)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_a_city(city_id):
    """ this method updates a state """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    req = request.get_json()
    if not request.is_json:
        abort(400, description="Not a JSON")
    for k, value in req.items():
        if k is not "id" and k is not "created_at" and k is not "updated_at"\
           and k is not "state_id":
            setattr(city, k, value)
    city.save()
    return jsonify(city.to_dict()), 200
