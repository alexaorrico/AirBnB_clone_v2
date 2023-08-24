#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def state():
    """List all State object into a valid JSON"""
    list_obj = []
    dict_storage = storage.all(State)

    for key, value in dict_storage.items():
        list_obj.append(value.to_dict())
    return jsonify(list_obj)


@app_views.route('/states/<id>', methods=['GET'], strict_slashes=False)
def state_id(id):
    """Retrieves a State object by his id"""
    obj_state_id = storage.get(State, id)
    if obj_state_id is None:
        abort(404)
    return jsonify(obj_state_id.to_dict())


@app_views.route('/states/<id>', methods=['DELETE'], strict_slashes=False)
def state_delete(id):
    """Delete a State object by his id"""
    empty = {}
    obj_state_id = storage.get(State, id)
    if obj_state_id is None:
        abort(404)
    storage.delete(obj_state_id)
    storage.save()
    return (jsonify(empty), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_create():
    """Returns the new State with the status code 201"""
    data = request.get_json()
    if data is None:
        return "Not a JSON\n", 400
    elif "name" not in data:
        return "Missing name\n", 400
    else:
        obj = State()
        obj.name = data["name"]
        storage.new(obj)
        storage.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/states/<id>', methods=['PUT'], strict_slashes=False)
def state_update(id):
    """Update a State object by his id"""
    obj_update = storage.get(State, id)
    if obj_update is None:
        abort(404)
    else:
        data = request.get_json()
        if data is None:
            return "Not a JSON\n", 400
        else:
            for key, value in data.items():
                if key not in ["id", "created_at", "updated_at"]:
                    setattr(obj_update, key, value)
            storage.save()

        return jsonify(obj_update.to_dict()), 200
