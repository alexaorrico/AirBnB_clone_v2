#!/usr/bin/python3
"""view for State objects that handles all default RestFul API actions"""
from api.v1.views import app_views
from models import storage
from models.state import State
from json import dumps
from api.v1.app import *
from flask import abort


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
