#!/usr/bin/python
"""holds class City"""
from models.state import State
from models.city import City
from flask import abort
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, request
from os import getenv
from models import storage
import json


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False,
                 methods=['GET'])
def all_cities(state_id):
    """grab all cities in a state"""
    cities = storage.all(City).values()
    obj = [city.to_dict() for city in cities if city.state_id == state_id]
    if len(obj) == 0:
        abort(404)
    return jsonify(obj)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['GET'])
def get_city_obj(city_id):
    """retrieve city obj"""
    cities = storage.all("City").values()
    obj = [city.to_dict() for city in cities if city.id == city_id]
    if len(obj) == 0:
        abort(404)
    return jsonify(obj)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """delete a city"""
    obj = storage.get("City", city_id)
    if obj is not None:
        storage.delete(obj)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False,
                 methods=['POST'])
def create_city(state_id):
    """create new city obj"""
    data = request.get_json()
    if 'name' not in data.keys():
        abort(404, "Missing name")
    if data is None:
        abort(400, "Not a JSON")
    new_city = City(**data)
    setattr(new_city, 'state_id', state_id)
    storage.new(new_city)
    storage.save()
    cities = storage.all(City)
    for city in cities.values():
        if city.state_id == state_id:
            return jsonify(new_city.to_dict()), 201
    abort(404)


@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=['PUT'])
def update_city(city_id):
    """create or update: idempotent"""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data.keys():
        abort(404, "Missing name")
    city = storage.get(City, city_id)
    for k, v in data.items():
        if k != "id" and k != "created_at" and k != "updated_at":
            setattr(city, k, v)
    city.save()
    return jsonify(city.to_dict())
