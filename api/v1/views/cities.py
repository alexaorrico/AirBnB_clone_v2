#!/usr/bin/python3
"""A new view for City objects that handlees all default
RESTFUL API actions"""
from flask import Flask, jsonify, request, abort
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_city_by_state_id(state_id):
    """Returns city or cities given it's/their
    State id if found else return 404"""
    state = storage.get(State, state_id)
    if state:
        cities = [c.to_dict() for c in state.cities]
        return jsonify(cities)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city_by_city_id(city_id):
    """Return a city given it's city id else 404"""
    city = storage.get(City, city_id)
    return jsonify(city.to_dict()) if city else abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city_object(city_id):
    """Deletes a city object if found otherwise return 404"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city_obj_by_state_id(state_id):
    """Creates a city object given a state id if state id is not
    linked to a state object return 404"""
    if not storage.get(State, state_id):
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    city = City(**data)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Updates a city object based on the city id"""
    fetch_city = storage.get(City, city_id)
    if fetch_city:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        keep = ["id", "created_at", "updated_at", "state_id"]
        for key, values in data.items():
            if key not in keep:
                setattr(fetch_city, key, values)
        fetch_city.save()
        return jsonify(fetch_city.to_dict()), 200
    else:
        abort(404)
