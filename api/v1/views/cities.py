#!/usr/bin/python3
"""new view for City objects that handles all default RESTFul API actions"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def city_index(state_id):
    if storage.get(State, state_id) is None:
        abort(404)
    all_cities = []
    state = storage.get(State, state_id)
    for city in state.cities:
        all_cities.append(city.to_dict())
    return jsonify(all_cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    if storage.get(City, city_id) is None:
        abort(404)
    return jsonify(storage.get(City, city_id).to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    cities = storage.all(City).values()
    for city in cities:
        if city.id == city_id:
            storage.delete(city)
            storage.save()
            return jsonify({}), 200
    return jsonify({'error': 'Not found'}), 404


@app_views.route('/states/<state_id>/cities/', methods=["POST"])
def post_city(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    try:
        info = request.get_json()
        if "name" not in info:
            return jsonify({"message": "Missing name"}), 400
        info['state_id'] = state.id
        city = City(**info)
        storage.new(city)
        storage.save()
        return jsonify(city.to_dict()), 201
    except Exception:
        return jsonify({"message": "Not a JSON"}), 400


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    try:
        info = request.get_json()
        for key, value in info.items():
            if key not in ["id", "state_id", "created_at", "updated_at"]:
                setattr(city, key, value)
            storage.save()
            return (city.to_dict(), 200)
    except Exception:
        return jsonify({"message": "Not a JSON"}), 400
