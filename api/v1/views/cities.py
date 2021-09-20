#!/usr/bin/python3
"""module for cities view"""
from flask import abort, request, jsonify, make_response
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City

@app_views.route("/states/<string:state_id>/cities", strict_slashes=False, methods=["GET"])
def get_state_cities(state_id):
    """retrive cities of a state"""
    required_state = storage.get(State, state_id)
    if (not required_state):
        abort(404)
    result = []
    for city in required_state.cities:
        result.append(city.to_dict())
    return jsonify(result)


@app_views.route("/cities/<string:city_id>", strict_slashes=False, methods=["GET"])
def get_city(city_id):
    """retrives a city instance"""
    required_city = storage.get(City, city_id)
    if (not required_city):
        abort(404)
    return jsonify(required_city.to_dict())


@app_views.route("/cities/<string:city_id>", strict_slashes=False, methods=["DELETE"])
def delete_city(city_id):
    """deletes a city instance"""
    required_city = storage.get(City, city_id)
    if (not required_city):
            abort(404)
    storage.delete(required_city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<string:state_id>/cities", strict_slashes=False, methods=["POST"])
def create_city(state_id):
    """creates a city"""
    required_state = storage.get(State, state_id)
    if (not required_state):
        abort(404)
    if not request.json:
        return make_response("Not a JSON", 400)
    if not 'name' in request.json:
        return make_response("Missing name", 400)

    properties = request.get_json()
    properties["state_id"] = state_id
    new_city = City(**properties)
    new_city.save()
    return new_city.to_dict(), 201


@app_views.route("/cities/<string:city_id>", strict_slashes=False, methods=["PUT"])
def edit_city(city_id):
    """edits a city"""
    required_city = storage.get(City, city_id)
    if (not required_city):
        abort(404)
    if not request.json:
        return make_response("Not a JSON", 400)
    
    input_dict = request.get_json()
    for key, value in input_dict.items():
        if (key not in ["id", "created_at", "updated_at"]):
            if (hasattr(required_city, key)):
                setattr(required_city, key, value)
    required_city.save()
    return required_city.to_dict(), 200
