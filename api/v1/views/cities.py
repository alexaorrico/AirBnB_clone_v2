#!/usr/bin/python3
""" Configures RESTful api for the cities route """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"],
                 strict_slashes=False)
def state_cities(state_id):
    """ configures the cities route """

    state = storage.get("State", state_id)

    if not state:
        abort(404)

    if request.method == "GET":
        state_cities = [city.to_dict() for city in state.cities]

        return jsonify(state_cities)
    else:
        try:
            json_dict = request.get_json()
        except Exception:
            abort(400, "Not a JSON")

        try:
            name = json_dict["name"]
        except KeyError:
            abort(400, "Missing name")

        new_city = City()
        new_city.name = name
        new_city.state_id = state_id

        storage.new(new_city)
        storage.save()

        return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def city_id(city_id):
    """ configures the cities/<city_id> route """

    city = storage.get("City", city_id)

    if not city:
        abort(404)

    if request.method == "GET":
        return jsonify(city.to_dict())
    elif request.method == "DELETE":
        storage.delete(city)
        storage.save()

        return jsonify({}), 200
    else:
        try:
            json_dict = request.get_json()
        except Exception:
            abort(400, "Not a JSON")

        keys_to_ignore = ["id", "created_at", "updated_at"]
        for key, val in json_dict.items():
            if key not in keys_to_ignore:
                setattr(city, key, val)

        storage.new(city)
        storage.save()

        return jsonify(city.to_dict()), 200
