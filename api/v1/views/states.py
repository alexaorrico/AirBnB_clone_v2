#!/usr/bin/python3
"""states conf"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def states():
    """method that returns all state objects"""
    list_objs = []
    objs = storage.all(State)
    for obj in objs.values():
        list_objs.append(obj.to_dict())
    return jsonify(list_objs)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """method that returns a state obj based on id or 404"""
    objs = storage.all(State)
    for obj in objs.values():
        if obj.id == state_id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    """method that deletes a state obj based on id or 404"""
    objs = storage.all(State)
    for obj in objs.values():
        if obj.id == state_id:
            obj.delete()
            storage.save()
            return jsonify({}), 200
    abort(404)
