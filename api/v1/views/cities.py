#!/usr/bin/python3
"""
City instance
"""

from crypt import methods
from flask import Flask, jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.state import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def cities_state(state_id):
    """Retrieves the list of all City objects of a State"""

    cities = []
    state = storage.get("State", state_id)

    if state is None:
        abort(404)

    for city in state.cities:
        cities.append(city.to_dict())

    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
def city(city_id):
    """Retrieves a City object"""

    city = storage.get("City", city_id)

    if city is None:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a city instance"""
    city = storage.get("City", city_id)

    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City instance"""
    body = request.get_json()

    if body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif "name" not in body.keys():
        return make_response(jsonify({"error": "Missing name"}), 400)

    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    else:
        city = City(**body)
        city.state_id = state_id
        city.save()
        return make_response(jsonify(city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"],
                 strict_slashes=False)
def update_city(city_id):
    """Updates a City instance"""

    body = request.get_json()
    no_update = ["id", "state_id", "created_at", "updated_at"]

    if body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    city = storage.get("City", city_id)

    if city is None:
        abort(404)
    else:
        for key, value in body.items():
            if key not in no_update:
                setattr(city, key, value)
            else:
                pass

        storage.save()
        return make_response(jsonify(city.to_dict()), 200)
