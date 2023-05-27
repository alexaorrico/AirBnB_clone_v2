#!/usr/bin/python3
"""
Module contains all endpoints to GET, POST, PUT OR DELETE
objects from State model.
"""
from models import storage
from models.state import State
from flask import jsonify
from api.v1.views import app_views
from flask import abort


@app_views.route("/states", strict_slashes=False)
def get_all_states():
    """
    Retrieves the list of all State objects
    """
    objs = storage.all(State).values()
    states = [obj.to_dict() for obj in objs]
    return jsonify(states)


@app_views.route("/states/<id>", methods=["GET"], strict_slashes=False)
def get_state_by_id(id):
    """
    Retrieves a State object by id
    """
    obj = storage.get(State, id)
    if obj:
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route("/states/<id>", methods=["DELETE"], strict_slashes=False)
def delete_state_by_id(id):
    """
    Deletes a State object by id
    """
    obj = storage.get(State, id)
    if obj:
        obj.delete()
        return jsonify({}), 200
    else:
        abort(404) 
