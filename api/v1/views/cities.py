#!/usr/bin/python3
"""CRUD methods in the city"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.city import City
from flask import abort
from flask import make_response
from flask import request
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Return cities of a given state"""
    if state_id:
        dic_state = storage.get(State, state_id)
        if dic_state is None:
            abort(404)
        else:
            cities = storage.all(City).values()
            list_cities = []
            for city in cities:
                if city.state_id == state_id:
                    list_cities.append(city.to_dict())
            return jsonify(list_cities)


@app_views.route('cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Return a single city based on the id"""
    if city_id:
        dic_city = storage.get(City, city_id)
        if dic_city is None:
            abort(404)
        else:
            return jsonify(dic_city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a city based on an id"""
    if city_id:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        else:
            storage.delete(city)
            storage.save()
            return make_response(jsonify({}), 200)


@app_views.route('states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Posts a city"""
    if state_id:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)

        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        reque = request.get_json()
        if "name" not in reque:
            return make_response(jsonify({"error": "Missing name"}), 400)
        reque['state_id'] = state_id
        city = City(**reque)
        city.save()
        return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Update a given city"""
    if city_id:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)

        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        reque = request.get_json()
        for key, value in reque.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(city, key, value)
        city.save()
        return make_response(jsonify(city.to_dict()), 200)
