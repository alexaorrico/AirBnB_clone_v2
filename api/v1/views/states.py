#!/usr/bin/python3
"""view for State objects that handles all default RESTFul API actions"""
from flask import jsonify
from flask import abort
from flask import request
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'])
def states():
    """Retrieves the list of all State objects"""
    try:
        States = storage.all(State)
        StateList = []
        for k in States:
            StateList.append(States[k].to_dict())
        return jsonify(StateList)
    except:
        abort(404)


@app_views.route("/states/<string:state_id>", methods=['GET'])
def getMethod(state_id):
    """Retrieves a State object"""
    try:
        state = storage.get(State, state_id).to_dict()
        return jsonify(state)
    except:
        abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'])
def deleteMethod(state_id):
    """Deletes a State object"""
    try:
        storage.delete(State, state_id)
        storage.save()
        return {}, 200
    except:
        abort(404)


@app_views.route("/states", methods=['POST'], endpoint='statesPost')
def postMethod():
    """Creates a State"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    instance = State(**data)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'])
def putMethod(state_id):
    """Updates a State object"""
    k = "State." + str(state_id)
    if k not in storage.all():
        abort(404)
    data = request.get_json()
    if not request.is_json:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(storage.all()[k], key, value)
    storage.all()[k].save()
    return jsonify(storage.get(State, state_id).to_dict()), 200
