#!/usr/bin/python3
"""api end point
"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.city import City
import json


@app_views.route('/cities', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT', 'POST'])
@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT', 'POST'])
def states(city_id=None):
    """display the states and cities listed in alphabetical order"""
    _states = storage.all("City")
    _state_id = storage.get("City", city_id)

    if request.method == 'GET':
        if not state_id:
            states_list = [state.to_dict() for state in _states.values()]
            return jsonify(states_list)
        if not _state_id:
            abort(404)
        return jsonify(_state_id.to_dict())

    if request.method == 'DELETE':
        if not _state_id:
            abort(404)
        storage.delete(_state_id)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'POST':
        try:
            data = request.get_json()
        except Exception as error:
            abort(400, "Not a JSON")

        if "name" not in data:
            return make_response("Missing name", 400)

        new = State(**data)
        storage.new(new)
        storage.save()
        return make_response(jsonify(new.to_dict()), 201)

    if request.method == 'PUT':
        try:
            data = request.get_json()
        except Exception as error:
            abort(400, "Not a JSON")

        if not _state_id:
            abort(404)

        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(_state_id, key, value)
        storage.save()
        return make_response(jsonify(_state_id.to_dict()), 200)
