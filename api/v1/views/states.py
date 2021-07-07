#!/usr/bin/python3
""" states view class """
from models import storage
from api.v1.views import app_views
from models.state import State
from flask import jsonify, request, abort, make_response


@app_views.route('/states', strict_slashes=False, methods=["GET", "POST"])
def get_states():
    """ to get all states or create new"""
    states = storage.all("State")
    if request.method == "GET":
        return jsonify([obj.to_dict() for obj in states.values()])
    if request.method == "POST":
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if request.get_json().get("name") is None:
            return make_response(jsonify({'error': 'Missing name'}), 400)
        state = State(**request.get_json())
        state.save()
        return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<string:state_id>', strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def get_state_id(state_id=None):
    """ get certain state """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == "GET":
        return jsonify(state.to_dict())
    if request.method == "PUT":
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for key, val in request.get_json().items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, val)
        state.save()
        return jsonify(state.to_dict())
    if request.method == "DELETE":
        state.delete()
        storage.save()
        return jsonify({})
