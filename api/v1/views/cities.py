#!/usr/bin/python3
"""City RESTAPI"""
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def get_cities(state_id):  # Get all cities of a state
    state = storage.get(State, state_id)
    if state:
        return jsonify([city.to_dict() for city in state.cities])
    abort(404)


@app_views.route("/cities/<city_id>/", strict_slashes=False)
def get_city(city_id):  # get a specific city
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route("/cities/<string:city_id>",
                 strict_slashes=False, methods=["DELETE"])
def delete_city(city_id):  # Delete a city
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route(
    "/states/<string:state_id>/cities", strict_slashes=False, methods=["POST"]
)
def create_city(state_id):  # Create a city in a state
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if "name" not in data:
        abort(400, description="Missing name")
    new_city = City(**data)
    new_city.state_id = state_id
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route("/cities/<string:city_id>",
                 strict_slashes=False, methods=["PUT"])
def update_city(city_id):  # Update a city
    city = storage.get(City, city_id)
    if city:
        data = request.get_json()
        if not data:
            abort(400, description="Not a JSON")
        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at", "state_id"]:
                setattr(city, key, value)
        storage.save()
        return make_response(jsonify(city.to_dict()), 200)
    abort(404)
