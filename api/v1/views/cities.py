#!/usr/bin/python3
"""
new view for City objects that handles all default RESTFul API actions
"""
from models import storage
from models.state import State
from models.city import City

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views


@app_views.route('/states/<string:state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_city(state_id):
    """retrieve a list of all City objects of a State"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    all_cities = []
    for city in state.cities:
        all_cities.append(city.to_dict())
    return jsonify(all_cities)


@app_views.route('/cities/<string:city_id>',
                 methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    """retrieve a city of a given id"""
    city = storage.get("City", city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<string:city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """deletes a city"""
    city = storage.get("City")
    if city:
        city.delete()
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/<string:state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """creates a city"""
    states = storage.all("State")
    if not request.is_json:
        abort(400, 'Not a JSON')
    else:
        request_body = request.get_json()

    if 'name' not in request_body:
        abort(400, 'Missing name')
    else:
        state_key = "State." + state_id
        if state_key not in states:
            abort(404)
        request_body.update({"state_id": state_id})
        new_city = City(**request_body)
        storage.new(new_city)
        storage.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<int:city_id>',
                 methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Updates a City object"""
    cities = storage.all("City")
    k = "City." + city_id
    try:
        city = cities[k]
    except KeyError:
        abort(404)
    if not request.is_json():
        abort(400, "Not a JSON")
    else:
        new = request.get_json()
    for k, v in new.items():
        if k != id and k != "state_id" and\
                k != "created_at" and k != "updated_at":
            setattr(city, k, v)
        storage.save()
