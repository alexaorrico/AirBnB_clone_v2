#!/usr/bin/python3
"""this module handles all default RESTFul API actions for the State"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage


@app_views.route('/states/', methods=['GET'])
def get_states():
    """retrieves all State objects"""
    dic = ([state.to_dict() for state in storage.all(State).values()])
    return (jsonify(dic))


@app_views.route('/states/<id>', methods=['GET'])
def get_state(id):
    """retrieves one State objects"""
    obj = storage.get(State, id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/states/<id>', methods=['DELETE'])
def delete_state(id):
    """deletes a state object"""
    obj = storage.get(State, id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/', methods=['POST'])
def create_state():
    """create a new state object"""
    if not request.get_json():
        abort(400, "Not a JSON")

    if 'name' not in request.get_json():
        abort("Missing name")

    new = State()
    new.name = request.get_json()['name']
    storage.new(new)
    storage.save()

    return (jsonify(new.to_dict()), 201)


@app_views.route('/states/<id>', methods=['PUT'])
def update_state(id):
    """update state object"""
    dic = request.get_json()
    obj = storage.get(State, id)
    if obj is None:
        abort(404)

    if not dic:
        abort(400, "Not a JSON")
    for key, value in dic.items():
        if key is not "created_at" and key is not "updated_at":
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200