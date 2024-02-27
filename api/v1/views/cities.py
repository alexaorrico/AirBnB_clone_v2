#!/usr/bin/python3
"""
Routes for handling State objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def get_cities_by_state(state_id):
    """
    Retrieves all City objects from a specific state.

    :param state_id: The ID of the state
    :return: JSON of all cities in a state or 404 on error
    """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route("/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def create_city(state_id):
    """
    Create a city route.

    :param state_id: The ID of the state
    :return: Newly created city object
    """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')

    if "name" not in city_json:
        abort(400, 'Missing name')

    city_json["state_id"] = state_id

    new_city = City(**city_json)
    new_city.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city_by_id(city_id):
    """
    Get a specific City object by ID.

    :param city_id: The ID of the city object
    :return: City object with the specified ID or error
    """
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city_by_id(city_id):
    """
    Update a specific City object by ID.

    :param city_id: The ID of the city object
    :return: City object and 200 on success, or 400 or 404 on failure
    """
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')

    for key, val in city_json.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(city, key, val)

    city.save()
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city_by_id(city_id):
    """
    Delete a City by ID.

    :param city_id: The ID of the city object
    :return: Empty dictionary with 200 or 404 if not found
    """
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()

    return jsonify({}), 200
