#!/usr/bin/python3
"""Defines views for cities module"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_city_by_state(state_id):
    """Retrieves a dict of cities of a state.
        methods::
                - GET: retrieve specified state.
                - POST: Creates new specified state
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    if request.method == "GET":
        return jsonify([city.to_dict() for city in state.cities])

    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    if data.get("name") is None:
        return "Missing name", 400
    #replaced setattr
    data["state_id"] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_city_by_id(city_id):
    """Retrieves, Deletes or Updates a city object by it's id
        methods::
                - GET: retrieve specified city.
                - PUT: Updates specified city with info
                - DELETE: Deletes specified city instance
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    if request.method == "GET":
        return jsonify(city.to_dict())

    elif request.method == "DELETE":
        city.delete()
        storage.save()
        return jsonify({})

    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    nope = {"id", "state_id", "created_at", "updated_at"}
    [setattr(city, k, v) for k, v in data.items() if k not in nope]
    city.save()
    return jsonify(city.to_dict())
