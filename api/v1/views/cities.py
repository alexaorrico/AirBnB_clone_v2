#!/usr/bin/python3
""" Create a new view for State objects
that handles all default RestFul API actions """
from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, abort, request
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def getcities(state_id=None, city_id=None):
    """GET cities"""
    if city_id:
        if storage.get(City, city_id):
            return jsonify(storage.get(City, city_id).to_dict())
        else:
            abort(404)
    if state_id:
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        alllist = []
        for cities in state.cities:
            alllist.append(cities.to_dict())
        return jsonify(alllist)
    else:
        abort(404)


@app_views.route(
    '/cities/<cities_id>', methods=['DELETE'],
    strict_slashes=False)
def deletestate(state_id=None):
    """DELETE state"""
    if storage.get(City, city_id):
        storage.delete(storage.get(City, city_id))
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/cities', methods=['POST'], strict_slashes=False)
def poststate():
    """POST state """
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    elif "name" not in body.keys():
        abort(400, "Missing name")
    else:
        post_city = City(**body)
        storage.save()
        return jsonify(post_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def putstate(city_id=None):
    """PUT state """
    city = storage.get("State", city_id)
    if city is None:
        abort(404)
    new = request.get_json()
    if new is None:
        abort(400, "Not a JSON")
    for key, value in new.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
