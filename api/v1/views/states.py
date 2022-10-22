#!/usr/bin/python3

"""Module to handle state request Blueprint"""

from email import message
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage, storage_t
from models.state import State

# @app_views.errorhandler(400)
# def handle_400(e):
#     return make_response(jsonify({"error": e}), 400)

# @app_views.errorhandler(404)
# def handle_404(e):
#     return make_response(jsonify({"error": e}), 400)


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def get_states():
    """return json array of all states"""
    if request.method == 'GET':
        states = storage.all(State)
        return jsonify([val.to_dict() for val in states.values()])
    if request.method == 'POST':
        try:
            body = request.get_json()
        except:
            return make_response({"error": "Not a JSON"}, 400)
            # abort(400, description="Not a JSON")
        if "name" not in body.keys():
            return make_response({"error": "Missing name"}, 404)
            # abort(404, message="Missing name")
        if storage_t != 'db':
            new_state = State(body["name"])
        else:
            new_state = State(name=body["name"])

        new_state.save()
        if storage.get(State, new_state.id) is not None:
            response = make_response(new_state.to_dict())
            response.status_code = 201
            return response


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_state(state_id):
    """Method to get, delete or modify a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())
    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({})
    if request.method == 'PUT':
        try:
            body = request.get_json()
        except:
            return make_response({"error": "Not a JSON"}, 400)
        _exceptions = ["id", "created_at", "updated_at"]
        for k, v in body.items():
            if k not in _exceptions:
                setattr(state, k, v)
                # state[k] = v
        state.save()
        return make_response(state.to_dict(), 200)
