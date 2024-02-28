#!/usr/bin/python3
"""This handles views for states"""
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, request, abort
import json


@app_views.route(
        '/states/<state_id>/cities',
        methods=['GET'],
        strict_slashes=False
        )
def all_cities(state_id):
    """This returns all cities"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = state.cities
    cities_list = [city.to_dict() for city in cities]
    return json.dumps(cities_list, indent=2)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_id(city_id):
    """Returns the city with that id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return json.dumps(city.to_dict(), indent=2)


@app_views.route(
        '/cities/<city_id>',
        methods=['DELETE'],
        strict_slashes=False
        )
def delete_city(city_id):
    """This deletes a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return json.dumps({}), 200


@app_views.route(
        '/states/<state_id>/cities',
        methods=['POST'],
        strict_slashes=False
        )
def create_city(state_id):
    """This function creates a city"""
    city_to_create = request.get_json()
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    elif not city_to_create:
        abort(400, "Not a JSON")
    elif "name" not in city_to_create:
        abort(400, "Missing name")
    city_to_create["state_id"] = state_id
    new_city = City(**city_to_create)
    new_city.save()
    return json.dumps(new_city.to_dict(), indent=2), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data_to_put = request.get_json()
    if not data_to_put:
        abort(400, "Not a JSON")
    for key, value in data_to_put.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, value)
    storage.save()
    return json.dumps(city.to_dict(), indent=2), 200
