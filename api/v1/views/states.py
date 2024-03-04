#!/usr/bin/python3
"""
View for State objects that handles all default RESTFul API actions.
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, State
from werkzeug.exceptions import BadRequest


@app_views.route("/states", strict_slashes=False)
def retrieve_all_objs():
    """returns a list of all state objects"""
    state_dict = storage.all(State)
    states_list = []
    for obj in state_dict.values():
        obj_dict = obj.to_dict()
        states_list.append(obj_dict)
    return states_list


@app_views.route("states/<state_id>", strict_slashes=False)
def retrieve_obj(state_id):
    """returns an object of a specified id"""
    state_dict = storage.all(State)
    for obj in state_dict.values():
        if obj.id == state_id:
            return obj.to_dict()
    # obj not found
    abort(404)


@app_views.route("/states/<state_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_obj(state_id):
    """removes an object from storage"""
    objs = storage.all(State)
    data = {}
    for obj in objs.values():
        if obj.id == state_id:
            # delete obj and save changes to storage
            storage.delete(obj)
            storage.save()
            return jsonify(data), 200
    # obj not found
    abort(404)


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def create_state():
    try:
        data = request.get_json()
    except BadRequest:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, 'Missing name')
    # create state object
    for v in data.values():
        state_obj = State(name=v)
    storage.new(state_obj)
    storage.save()
    obj_dict = state_obj.to_dict()
    return jsonify(obj_dict), 201


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_obj(state_id):
    """update a state object"""
    objs = storage.all(State)
    for obj in objs.values():
        if obj.id == state_id:
            try:
                data = request.get_json()
            except BadRequest:
                abort(400, 'Not a JSON')
            for k, v in data.items():
                # update value
                setattr(obj, k, v)
            # save changes to storage
            storage.save()
            state_obj = obj.to_dict()
            return jsonify(state_obj), 201
    # object not found
    abort(404)
