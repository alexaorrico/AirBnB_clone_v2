#!/usr/bin/python3
"""view for State objects that handles all default RestFul API actions"""
from api.v1.views import app_views
from models import storage
from models.state import State
from json import dumps
from api.v1.app import *
from flask import abort, request


@app_views.route('/states/')
def all_states():
    """Retrieves the list of all State"""
    dict_states = storage.all(State)
    object_list = []
    for value in dict_states.values():
        obj = value.to_dict()
        object_list.append(obj)
    object_list = dumps(object_list, indent=4)
    return (object_list)


@app_views.route('/states/<id>')
def states_by_id(id):
    """retrieves the state by the given id """
    dict_states = storage.all(State)
    key = "State." + id
    obj = None
    if key in dict_states:
        obj = dict_states[key].to_dict()
    if obj is None:
        abort(404)
    obj = dumps(obj, indent=4)
    return (obj)


@app_views.route('/states/<id>', methods=['DELETE'])
def delete_by_id(id):
    """delete state by id"""
    dict_states = storage.all(State)
    key = "State." + id
    if key in dict_states:
        obj = dict_states[key]
        obj.delete()
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/states/', methods=['POST'])
def post_state():
    """get request and post new state"""
    new_state = None
    try:
        new_state = request.get_json()
        if 'name' in new_state:
            obj_state = State()
            obj_state.name = new_state['name']
            storage.new(obj_state)
            storage.save()
            dict_obj = obj_state.to_dict()
            return dumps(dict_obj, indent=4)
        else:
            return 'Missing name', 400
    except:
        return 'Not a JSON', 400


@app_views.route('/states/<id>', methods=['PUT'])
def edit_by_id(id):
    """edit state by id"""
    try:
        dict_states = storage.all(State)
        new_state = request.get_json()
        key = "State." + id
        if key in dict_states:
            obj = dict_states[key]
            obj.name = new_state["name"]
            storage.save()
            obj = obj.to_dict()
            return dumps(obj, indent=4)
        else:
            abort(404)
    except:
        return 'Not a JSON', 400
