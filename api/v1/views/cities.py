#!/usr/bin/python3
"""
This is the module for cities
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def all_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    obj_state = storage.get(State, state_id)
    if not obj_state:
        abort(404)
    cities = [city.to_dict() for city in obj_state.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def one_city(city_id):
    """Retrieves a City object"""
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)

    return jsonify(obj.to_dict())


@app_views.route("/api/v1/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def del_city(city_id):
    """Returns an empty dictionary with status code 200"""
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route(
    "/api/v1/states/<state_id>/cities", methods=["POST"], strict_slashes=False
)
def create_city(state_id):
    """Creates one city with the state_id given"""
    obj_state = storage.get(State, state_id)
    if not obj_state:
        abort(404)

    new_city = request.get_json()
    if not new_city:
        abort(400, "Not a JSON")
    if "name" not in new_city:
        abort(400, "Missing name")

    obj = City(**new_city)
    obj.state_id = state_id
    obj.save()

    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """Updates one city tied with the given state_id"""
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)

    rq = request.get_json()
    if not rq:
        abort(400, "Not a JSON")

    for key, value in rq.items():
        if key not in ["id", "created_at", "update_at", "state_id"]:
            setattr(obj, key, value)

    return make_response(jsonify())
