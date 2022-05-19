#!/usr/bin/python3
""" City """
import json
from models import storage
from flask import jsonify, abort, request, make_response
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities", methods=['GET', 'POST'],
                 strict_slashes=False)
def cities(state_id):
    """ DO some method on City with a state_id """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if request.method == 'GET':
        list_cities = []
        for city in state.cities:
            list_cities.append(city.to_dict())
        return jsonify(list_cities)

    if request.method == 'POST':
        response = request.get_json()
        if response is None:
            abort(400, "Not a JSON")
        if response.get("name") is None:
            abort(400, "Missing name")

        new = City(**response)
        new.state_id = state.id
        new.save()
        return make_response(jsonify(new.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def city_id(city_id):
    """ Do different methods on a City object"""
    city = storage.get(State, city_id)
    if not city:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    elif request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({})

    elif request.method == 'PUT':
        ignore = ["id", "created_at", "updated_at"]
        response = request.get_json()
        if response is None:
            abort(400, "Not a JSON")
        for key, value in response.items():
            if key not in ignore:
                setattr(city, key, value)
        storage.save()
        return make_response(jsonify(city.to_dict()), 200)
