#!/usr/bin/python3
""" new view for State objects """

from models.state import State
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage, base_model


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states():
    """Retrieves the list of all State objects"""
    if request.method == 'GET':
        state_list = []
        for ob in storage.all(State).values():
            state_list.append(ob.to_dict())
        return jsonify(state_list), 200


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state_id(state_id):
    """Retrieves a State by id"""
    if request.method == 'GET':
        ob = storage.get(State, state_id)
        if ob is not None:
            return jsonify(ob.to_dict())
        else:
            return jsonify({"error": "Not found"}), 404


@app_views.route(
    '/states/<state_id>',
    strict_slashes=False,
    methods=['DELETE']
)
def delete_state_ob(state_id):
    """Delete a State object by id"""
    if request.method == 'DELETE':
        ob = storage.get(State, state_id)
        if ob is not None:
            storage.delete(ob)
            storage.save()
            return jsonify({}), 200
        else:
            return abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state_ob():
    """Create a State object"""
    if request.method == 'POST':
        test = request.get_json()
        if not test:
            return "Not a JSON", 400
        elif "name" not in test:
            return "Missing name", 400
        else:
            ob = State(**test)
            storage.new(ob)
            storage.save()
            return jsonify(ob.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state_ob(state_id):
    """Update a State object"""
    if request.method == 'PUT':
        ob = storage.get(State, state_id)
        data = request.get_json()
        if not ob:
            return abort(404)
        if not data:
            return "Not a JSON", 400
        for key, val in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(ob, key, val)
        storage.save()
        return jsonify(ob.to_dict()), 200
