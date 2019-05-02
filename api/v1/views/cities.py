#!/usr/bin/python3
""" Cities view for HBNB API """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City

import json


@app_views.route("/states/<state_id>/cities",
                 methods=["GET", "POST"], strict_slashes=False)
def city_list(state_id):
    """ GET: render a list of cities
        POST: Create a city
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if request.method == "POST":
        new_dict = request.get_json(silent=True)
        if not new_dict:
            return jsonify({"error": "Not a JSON"}), 400
        if "name" not in request.json:
            return jsonify({"error": "Missing name"}), 400
        new_dict["state_id"] = state_id
        city = City(**new_dict)
        storage.new(city)
        storage.save()
        storage.close()
        return jsonify(city.to_dict()), 201
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def city_detail(city_id):
    """ GET: Return a json of a city detail
        DELETE: Deltes an object and returns an empty json dictionary
        PUT: Updates a city
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.method == "DELETE":
        storage.delete(city)
        storage.save()
        storage.close()
        return jsonify({})
    elif request.method == "PUT":
        new_dict = request.get_json(silent=True)
        if not new_dict:
            return jsonify({"error": "Not a JSON"}), 400
        for k, v in new_dict.items():
            if k not in ["id", "state_id", "created_at", "updated_at"]:
                setattr(city, k, v)
        storage.new(city)
        storage.save()
        storage.close()
    return jsonify(city.to_dict())
