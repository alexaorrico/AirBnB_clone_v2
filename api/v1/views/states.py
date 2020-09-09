#!/usr/bin/python3
"""New Funtion states"""
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, abort, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """ss"""
    list_dict = []
    for obj in storage.all(State).values():
        list_dict.append(obj.to_dict())
    return jsonify(list_dict), 200


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state_by_id(state_id):
    """ddd"""
    obj = storage.get(State, state_id)
    if (obj):
        return jsonify(obj.to_dict()), 200
    else:
        abort(404)


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_by_id(state_id):
    """delete method api"""
    obj = storage.get(State, state_id)
    if (obj):
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state_create():
    """comet"""
    conten = request.get_json()
    if conten is None:
        return "Not a JSON", 400
    if conten.get('name') == None:
        return "Missing name", 400
    else:
        new_obj = State(**conten)
        storage.new(new_obj)
        storage.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'], strict_slashes=False)
def put_state_update(state_id):
    """comet"""
    obj = storage.get(State, state_id)
    conten = request.get_json()

    if obj == None:
        return abort(404)
    if conten is None:
        return "Not a JSON", 400
    if conten.get('name') == None:
        return "Missing name", 400
    obj.__dict__ = conten
    storage.save()
    return jsonify(obj.to_dict()), 200

""" else:
        obj.__dict__ = conten
        storage.new(obj)
        storage.save() """