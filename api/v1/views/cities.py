#!/usr/bin/python3
"""
Create a new view for City objects that
handles all default RESTFul API actions
"""

from flask import Flask, request, jsonify, abort
from models import storage
from api.v1.views import app_views
from models.state import State
from models.city import City

app = Flask(__name__)


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def get_cities_by_state(state_id):
    store_states = storage.get(State, state_id)
    if store_states is None:
        return abort(404)
    list_cities = [city.to_dict() for city in store_states.cities]
    return jsonify(list_cities)


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                strict_slashes=False)
def post_cities(state_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    store_states_id = storage.get(State, state_id)
    if store_states_id is None:
        return abort(404)
    data["state_id"] = store_states_id.id
    new_city = City(**data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_cities_id(city_id):
    store_cities = storage.get(City, city_id)
    if store_cities is None:
        return abort(404)
    return jsonify(store_cities.to_dict())


@app_views.route('/cities/<city_id>', methods=['PUT'])
def put_cities_id(city_id):
    data = request.get_json()
    store_cities_id = storage.get(City, city_id)
    if store_cities_id is None:
        return abort(404)
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(store_cities_id, key, value)
    store_cities_id.save()
    return jsonify(store_cities_id.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_cities_id(city_id):
    to_delete = storage.get(City, city_id)
    if to_delete is None:
        return abort(404)
    storage.delete(to_delete)
    storage.save()
    return jsonify({}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
