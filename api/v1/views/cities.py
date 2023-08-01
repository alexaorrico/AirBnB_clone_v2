#!/usr/bin/python3
"""This is a module that contains views for the Cities for this API"""
from flask import jsonify
from flask import request
from flask import abort
from flask import make_response
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_state_cities(state_id):
    """This is a function that gets all cities in a state when the
    /states/state_id/cities route is reached"""
    all_cities = []
    state = storage.get(State, state_id)
    if state:
        for city in state.cities:
            all_cities.append(city.to_dict())
        return jsonify(all_cities)
    abort(404)


@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
def get_one_city(city_id):
    """This is a function that gets a city with a city id /cities/city_id
    route is reached"""
    result = storage.get(City, city_id)
    if result:
        return jsonify(result.to_dict())
    abort(404)


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_one_city(city_id):
    """this is a function that deletes a specified state when the
    /cities/city_id route is reached"""
    result = storage.get(City, city_id)
    if result:
        storage.delete(result)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """This is a function that creates a new city at the
    /states/state_id/cities route's endpoint"""
    result = storage.get(State, state_id)
    if result:
        if request.get_json():
            if 'name' in request.get_json():
                city = request.get_json()
                data = City(**city)
                data.state_id = state_id
                data.save
                return make_response(jsonify(data.to_dict()), 201)
            abort(400,  description="Missing name")
        abort(404, description="Not a JSON")
    abort(404)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_one_city(city_id):
    """This is a function that updates a specified city at the /cities/city_id
    route's endpoint"""
    result = storage.get(City, city_id)
    if not result:
        abort(404)
    if request.get_json():
        data = request.get_json()
        for item, val in data.items():
            if item not in ["id", "state_id", "created_at", "updated_at"]:
                setattr(result, item, val)
        storage.save()
        return make_response(jsonify(result.to_dict()), 200)
    abort(400, description="Not a JSON")
