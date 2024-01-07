#!/usr/bin/python3
"""
View for State objects that Handles all default RESTFul API
actions
"""
from models import storage
from models.state import State
from flask import Flask, abort, jsonify, request, make_response
from api.v1.views import app_views


@app_views.route('/api/v1/states', method=['GET'],
                 strictslashes=False)
def list_state_objects():
    """ """
    all_objs = storage.all(State)
    return [obj.to_dict() for obj in all_objs.values()]


@app_views.route('/api/v1/states/<state_id>', method=['GET'],
                 strictslashes=False)
def get_state_objects(state_id):
    """ """
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/api/v1/states/<state_id>', method=['DELETE'],
                 strictslashes=False)
def delete_state_objects(state_id):
    """ """
    obj = storage.get(State, state_id)
    if obj is None or not obj:
        abort(404)

    storage.delete(obj)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/api/v1/states', method=['POST'],
                 strictslashes=False)
def create_state():
    """ """
    data = request.get_json()

    if not data:
        abort(404, "Not a JSON")
    elif 'name' not in data.keys():
        abort(404, 'Missing name')

    obj = State(**data)
    storage.new(obj)
    storage.save()

    return make_response(jsonify(obj), 201)


@app_views.route('/api/v1/states/<state_id>', method=['PUT'],
                 strictslashes=False)
def update_state_objects(state_id):
    """ """
    obj = storage.get(State, state_id)

    if obj is None or not obj:
        abort(404)

    data = request.get_json()
    if not data:
        abort(404, "Not a JSON")

    storage.delete(obj)

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)

    storage.save()

    return make_response(jsonify(obj), 200)
