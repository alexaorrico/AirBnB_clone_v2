#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, Blueprint, render_template, abort, request
from models import storage
from models.state import State
from models.city import City
from models.base_model import BaseModel


@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"],
                 strict_slashes=False)
def get_cities(state_id):
    res = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == "GET":
        for city in state.cities:
            res.append(city.to_dict())
        return jsonify(res)
    if request.method == "POST":
        if not request.json:
            return jsonify({"error": "Not a JSON"}), 400
        if "name" not in request.json:
            return jsonify({"error": "Missing name"}), 400
        new_city.state_id = state_id
        new_city = City(**request.json)
        new_city.save()
        return (jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['GET', 'PUT'],
                 strict_slashes=False)
def put_cities(state_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
        if request.method == "GET":
            return jsonify(city.to_dict())
        if request.method == "PUT":
            if not request.json:
                return jsonify({"error": "Not a JSON"}), 400
            for key, value in request.json.items():
                setattr(city, key, value)
            city.save()
            return (jsonify(city.to_dict()), 200)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_cities(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
        city.delete()
    storage.save()
    return (jsonify({}), 200)
