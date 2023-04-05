#!/usr/bin/python3
"""
Module to create view for State objects handling default
RESTful API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<string:state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def cities_in_state(state_id):
    """
    Retrieves all City objects of a state with given id
    Raise 404 error if id not linked to any State object
    """
    state = storage.get(State, state_id)
    ret = []
    if state is None:
        abort(404)
    for city in state.cities:
        ret.append(city.to_dict())
    return make_response(jsonify(ret))


@app_views.route("/cities/<string:city_id>", methods=["GET"],
                 strict_slashes=False)
def city_id_get(city_id):
    """
    Retrieves a city with a given id
    Raise 404 error if id not linked to any City object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return make_response(jsonify(city.to_dict()))


@app_views.route("/cities/<string:city_id>", methods=["DELETE"],
                 strict_slashes=False)
def city_id_delete(city_id):
    """
    Deletes a City object with a given id
    Raise 404 error if id not linked to any City object
    Returns and empty dictionary with status code 200
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<string:state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def city_post(state_id):
    """
    Creates a City via POST
    If the state_id is not linked to any State object, raise a 404 error
    If the HTTP body request is not valid JSON, raise 400 error, Not a JSON
    If the dictionary doesn't contain the key name, raise a 400 error with
    message Missing name
    Returns new City with status code 201
    """
    state = storage.get(State, state_id)
    city_info = request.get_json()
    if state is None:
        abort(404)
    if not city_info:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in city_info.keys():
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_city = City(**city_info)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route("/cities/<string:city_id>", methods=["PUT"],
                 strict_slashes=False)
def city_put(city_id):
    """
    Updates a City object via PUT
    If the city_id is not linked to any City object, raise 404 error
    If the HTTP body request is not valid JSON, raise a 400 error, Not a JSON
    Update the City object with all key-value pairs of the dictionary
    Ignore keys: id, created_at, updated_at
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    ignore_keys = ["id", "created_at", "updated_at"]
    for key, value in request.get_json().items():
        if key not in ignore_keys:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
