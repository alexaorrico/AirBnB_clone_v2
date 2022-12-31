#!/usr/bin/python3
''' cities.py'''

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities",
                 methods=["GET", "POST"],
                 strict_slashes=False)
def get_cities(state_id):
    '''Retrieves the list of all City objects of a State'''
    state_object = storage.get(State, state_id)
    if not state_object:
        abort(404)

    if request.method == "GET":
        cities = [city.to_dict() for city in state_object.cities]
        return jsonify(cities)

    elif request.method == "POST":
        if not request.is_json:
            abort(400, description="Not a JSON")

        if "name" not in request.json:
            abort(400, description="Missing name")

        city_json = request.get_json()
        city_obj = City(state_id=state_id, **city_json)
        storage.new(city_obj)
        storage.save()

        return jsonify(city_obj.to_dict()), 201


@app_views.route("/cities/<city_id>",
                 methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def get_city_id(city_id):
    '''Retrieves a City object'''
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    if request.method == "GET":
        return jsonify(city.to_dict())

    elif request.method == "DELETE":
        storage.delete(city)
        storage.save()
        return jsonify({}), 200

    elif request.method == "PUT":
        if not request.is_json:
            abort(400, description="Not a JSON")

        city_json = request.get_json()
        not_needed = ["id", "created_at", "updated_at", "state_id"]
        for attr, attr_value in city_json.items():
            if attr not in not_needed:
                setattr(city, attr, attr_value)
        city.save()
        return jsonify(city.to_dict()), 200
