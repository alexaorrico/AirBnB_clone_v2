#!/usr/bin/python3
"""
    This module creates a new view for City
    objects that handles all default REST API
    actions.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities",
                 methods=['GET'], strict_slashes=False)
def get_cities_in_state(state_id):
    """Get cities in a given state"""
    state = storage.get(State, state_id)
    if state:
        cities = state.cities
        city_list = []
        for city in cities:
            city_list.append(city.to_dict())
        return jsonify(city_list)
    else:
        abort(404)


@app_views.route("/cities/<city_id>",
                 methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Get a specific city from the db"""
    search_result = storage.get(City, city_id)
    if search_result:
        return jsonify(search_result.to_dict())
    abort(404)


@app_views.route("/cities/<city_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Delete a specific city from the db"""
    search_result = storage.get(City, city_id)
    if search_result:
        storage.delete(search_result)
        storage.save()
        return jsonify({}), 200

    else:
        abort(404)


@app_views.route("/states/<state_id>/cities/", methods=['POST'],
                 strict_slashes=False)
def post_new_city(state_id):
    """Post a new city to the db"""
    state = storage.get(State, state_id)
    if state:
        try:
            city_dict = request.get_json()
            city_dict.update({"state_id": state_id})

        except Exception:
            return jsonify({"error": "Not a JSON"}), 400

        if city_dict.get("name"):
            new_city = City(**city_dict)
            storage.new(new_city)
            storage.save()
            return jsonify(new_city.to_dict()), 201

        return jsonify({"error": "Missing name"}), 400

    else:
        abort(404)


@app_views.route("cities/<city_id>", methods=['PUT'],
                 strict_slashes=False)
def modify_city(city_id):
    """Modify an existing city in the db"""
    city = storage.get(City, city_id)
    if city:
        try:
            update_dict = request.get_json()
            for key in ('id', 'created_at', 'updated_at'):
                if update_dict.get(key):
                    del update_dict[key]

        except Exception:
            return jsonify({"error": "Not a JSON"}), 400

        for key, value in update_dict.items():
            setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200

    else:
        abort(404)
