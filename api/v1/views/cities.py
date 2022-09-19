#!/usr/bin/python3
"""state view"""
from models.city import City
from models import storage
from flask import Flask, abort, jsonify, request, make_response
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def cities(state_id):
    """Return all cities  in state"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    allCities = []
    for city in state.cities:
        allCities.append(city.to_dict())
    return jsonify(allCities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city(city_id):
    """Retrieves a City object"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delet_city(city_id):
    """deletes a city object"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_cite(state_id):
    """ post cite"""
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    if 'name' not in req.keys():
        abort(400, "Missing name")
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    instance = City(**req)
    instance.state_id = state_id
    instance.save()
    make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_cite(city_id):
    """ put cite """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if request.get_json() is None:
        abort(400, "Not a JSON")
    req = request.get_json()
    for key, value in req.items():
        setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
