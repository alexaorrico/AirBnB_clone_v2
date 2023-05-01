#!/usr/bin/python3
"""
handles REST API actions for State
"""
from api.v1.views import app_views
from flask import jsonify
from flask import Flask
from flask import request
from flask import abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def state():
    """handles states route"""
    if request.method == 'GET':
        return jsonify(
            [obj.to_dict() for obj in storage.all("State").values()])
    if request.method == 'POST':
        post_data = request.get_json()
        if post_data is None or type(post_data) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        new_name = post_data.get('name')
        if new_name is None:
            return jsonify({'error': 'Missing name'}), 400
        new_state = State(**post_data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route(
    '/states/<string:state_id>',
    methods=['GET', 'DELETE', 'PUT'],
    strict_slashes=False)
def state_with_id(state_id):
    """handles states route with a parameter state_id"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())
    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        put_data = request.get_json()
        if put_data is None or type(put_data) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        to_ignore = ['id', 'created_at', 'updated_at']
        state.update(to_ignore, **put_data)
        return jsonify(state.to_dict()), 200
