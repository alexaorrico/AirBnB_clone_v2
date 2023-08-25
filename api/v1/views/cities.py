#!/usr/bin/python3
"""Flask application for cities class/entity"""
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, abort, request


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def retrieves_all_cities(state_id):
    """Returns the list of all City objects"""
    state = storage.get(State, state_id)
    if not state_id:
        abort(404)
    cities = state.cities
    cities_list = []
    for city in cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def retrieves_city(city_id):
    """Returns an object by id"""
    cities = storage.get(City, city_id)
    if not cities:
        abort(404)
    return jsonify(cities.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def deletes_city(city_id):
    """Deletes an object by id"""
    cities = storage.get(City, city_id)
    if not cities:
        abort(404)
    storage.delete(cities)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=["POST"],
                 strict_slashes=False)
def update_city(state_id):
    """Creates an Object"""
    city_data = request.get_json()
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    elif not city_data:
        abort(400, "Not a JSON")
    elif "name" not in city_data:
        abort(400, "Missing name")

    city_data["state_id"] = state_id
    new_city = City(**city_data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """Updates an object"""
    city_data = request.get_json()
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    elif not city_data:
        abort(400, "Not a JSON")

    for key, value in city_data.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
