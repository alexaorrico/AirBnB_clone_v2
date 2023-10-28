#!/usr/bin/python3
"""cities.py"""
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route("/states/<state_id>/cities", methods=['GET'])
def get_cities_by_state(state_id):
    """Retrieves all City objects of a State"""
    all_states = storage.all("State").values()
    state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if state_obj == []:
        abort(404)
    list_cities = [obj.to_dict() for obj in storage.all("City").values()
                   if state_id == obj.state_id]
    return jsonify(list_cities)


@app_views.route("/cities/<city_id>")
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=['POST'])
def post_city(state_id):
    """Creates a City"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    city = City(**data)
    city.state_id = state_id
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'])
def update_city(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}, 400)
    to_be_ignored = ["id", "state_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in to_be_ignored:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
