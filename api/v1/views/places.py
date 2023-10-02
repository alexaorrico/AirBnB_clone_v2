#!/usr/bin/python3
"""
    cities.py file in v1/views
"""
from flask import abort, Flask, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"], strict_slashes=False)
def handle_cities(state_id):
    """
        Method to return a JSON representation of cities by state
    """
    state_by_id = storage.get(State, state_id)
    if state_by_id is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        city_list = []
        for city in state_by_id.cities:
            city_list.append(city.to_dict())
        return jsonify(city_list)

    elif request.method == 'POST':
        post = request.get_json()
        if post is None or type(post) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        elif post.get('name') is None:
            return jsonify({'error': 'Missing name'}), 400

        state_by_id = storage.get(State, state_id)
        if not state_by_id:
            abort(404)

        new_state = City(**post)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def handle_cities_by_id(city_id):
    """
        Method to return a JSON representation of a city
    """
    city_by_id = storage.get(City, city_id)
    if city_by_id is None:
        abort(404)
    elif request.method == 'GET':
        return jsonify(city_by_id.to_dict())
    elif request.method == 'DELETE':
        storage.delete(city_by_id)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        put = request.get_json()
        if put is None or type(put) != dict:
            return jsonify({'message': 'Not a JSON'}), 400
        for key, value in put.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(city_by_id, key, value)
        storage.save()
        return jsonify(city_by_id.to_dict()), 200
