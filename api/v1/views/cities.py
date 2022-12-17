#!/usr/bin/python3
"""Module for city endpoints"""
from flask import jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def get_state_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if not state:
        return make_response(jsonify({"error": "Not found"}), 404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_cities(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if not city:
        return make_response(jsonify({"error": "Not found"}), 404)
    return jsonify(city.to_dict())


@app_views.route('cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if not city:
        return make_response(jsonify({"error": "Not found"}), 404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("states/<state_id>/cities",
                 strict_slashes=False, methods=["POST"])
def post_city(state_id):
    """POST /state API route"""
    state = storage.get(State, state_id)
    if not state:
        return make_response(jsonify({"error": "Not found"}), 404)

    data = request.get_json(force=True, silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)

    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"])
def put_city(city_id):
    """PUT /state API route"""
    city = storage.get(City, city_id)
    if not city:
        return make_response(jsonify({"error": "Not found"}), 404)
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
