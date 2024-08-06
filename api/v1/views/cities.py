#!/usr/bin/python3
"""handles all default RESTFul API actions for City objects"""

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route(
    "/states/<state_id>/cities", methods=["GET"], strict_slashes=False
)
def get_state_cities(state_id):
    """Retrieves all cities objects"""
    state_data = storage.get(State, state_id)
    if state_data is None:
        abort(404)
    cities = [city.to_dict() for city in state_data.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """Retrieves a  City object"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    # delete the city object
    city.delete()
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route(
    "/states/<state_id>/cities", methods=["POST"], strict_slashes=False
)
def create_city(state_id):
    """Creates a City object"""

    state_data = storage.get(State, state_id)
    if state_data is None:
        abort(404)

    new_city = request.get_json()

    # validate the posted city data
    if not new_city:
        abort(400, "Not a JSON")
    elif "name" not in new_city.keys():
        abort(400, "Missing name")
    else:
        new_city = City(**new_city)
        new_city.state_id = state_id
        new_city.save()

    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""

    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    new_city = request.get_json()

    if not new_city:
        abort(400, "Not a JSON")
    else:
        # update the city object
        for k, v in new_city.items():
            if k not in ["id", "state_id", "created_at", "updated_at"]:
                setattr(city, k, v)
        storage.save()

    # return the updated city
    return jsonify(city.to_dict())
