#!/usr/bin/python3
"""
    states.py file in v1/views
"""
from flask import abort, Flask, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET", "POST"], strict_slashes=False)
def handle_states():
    """
        Method to return a JSON representation of all states
    """
    if request.method == 'GET':
        return jsonify([val.to_dict() for val in storage.all('State')
                        .values()])
    elif request.method == 'POST':
        post = request.get_json()
        if post is None or type(post) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        elif post.get('name') is None:
            return jsonify({'error': 'Missing name'}), 400
        new_state = State(**post)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def handle_state_by_id(state_id):
    """
        Method to return a JSON representation of a state
    """
    state_by_id = storage.get(State, state_id)
    if state_by_id is None:
        abort(404)
    elif request.method == 'GET':
        return jsonify(state_by_id.to_dict())
    elif request.method == 'DELETE':
        storage.delete(state_by_id)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        put = request.get_json()
        if put is None or type(put) != dict:
            return jsonify({'message': 'Not a JSON'}), 400
        for key, value in put.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state_by_id, key, value)
        storage.save()
        return jsonify(state_by_id.to_dict()), 200
