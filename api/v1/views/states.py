#!/usr/bin/python3
""" new view for State objects """
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def allstates():
    """ GET all states """
    res = []
    for i in storage.all(State).values():
        res.append(i.to_dict())
    return jsonify(res)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def getstate(state_id):
    """ GET a state """
    s = storage.get(State, state_id)
    if s is None:
        abort(404)
    return jsonify(s.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletestate(state_id=None):
    """ DELETE a state """
    s = storage.get(State, state_id)
    if s is None:
        abort(404)
    else:
        storage.delete(s)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def createstate():
    """ CREATE a state """
    s = request.get_json(silent=True)
    if s is None:
        abort(400, "Not a Json")
    elif "name" not in s.keys():
        abort(400, "Missing name")
    else:
        new_s = State(**s)
        storage.new(new_s)
        storage.save()
        return jsonify(new_s.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def updatestate(state_id):
    """ update state with PUT """
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    s = request.get_json(silent=True)
    if s is None:
        abort(400, "Not a Json")
    for key, value in s.items():
        list_ignore = ["id", "created_at", "updated_at"]
        if key not in list_ignore:
            setattr(s, key, value)
            # setting attribute to be what's passed in
    s.save()
    return jsonify(s.to_dict()), 200
