#!/usr/bin/python3
""" Python script for City Routes & views"""
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, abort, request
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"])
def get_cities_by_state(state_id):
    """ Get methods for cities  routes"""
    # prepare the state obj
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    # get method
    if request.method == "GET":
        cities = []

        for city in state.cities:
            cities.append(city.to_dict())
        return jsonify(cities)

    # post method
    data = request.get_json(silent=True)
    if not data:
        return "Not a JSON", 400
    if "name" not in data:
        return "Missing name", 400

    # create new city object
    data["state_id"] = state_id

    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["GET", "DELETE", "PUT"])
def get_city_id(city_id):
    """ Get methods for retriving states objects by id"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    # DELETE method
    if request.method == "DELETE":
        city.delete()
        storage.save()
        return jsonify({}), 200

    # GET method
    elif request.method == "GET":
        return jsonify(city.to_dict())

    # PUT method
    data = request.get_json(silent=True)
    if not data:
        return "Not a JSON", 400
    keys_ignored = {"id", "created_at", "state_id" "updated_at"}
    [setattr(city, k, v) for k, v in data.items() if k not in keys_ignored]
    city.save()
    return jsonify(city.to_dict()), 200
