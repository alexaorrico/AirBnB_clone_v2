#!/usr/bin/python3
"""return states(s)"""
from api.v1.views import app_views
from models import storage
from models.state import State
import json
import flask
from flask import abort

@app_views.route('/states', strict_slashes=False)
def states():
    """retrieves all states"""
    states_array = []
    states = storage.all(State)
    for sts in states:
        states_array.append(states.get(sts).to_dict())
    return states_array

@app_views.route('/states/<string:state_id>', strict_slashes=False)
def state(state_id):
    """retrieves a specific state object"""
    state = storage.get(State, state_id)
    if state is None:
        data = {"error": "Not found"}
        return data, 404
    return jsonify(state.to_dict()), 200

@app_views.delete('/states/<state_id>', strict_slashes=False)
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state:
        storage.delete()
        storage.save()
        return {}, 200
    else:
        return {"error": "Not found"}, 404

@app_views.post('/states', strict_slashes=False)
def create():
    req = flask.request.get_json()
    try:
        json.dumps(req)
    except Exception as e:
        return "Not a JSON", 400
    if req.get("name"):
        r = State()
        r.name = req.get("name")
        storage.new(r)
        storage.save()
    else:
        return "Missing name", 400
    return r, 201

@app_views.put('/states/<state_id>', strict_slashes=False)
def update(state_id):
    state = storage.get(State, state_id)
    if state:
        abort(404)
    else:
        req = flask.request.get_json()
        try:
            json.dumps(req)
            r = State()
            print(dir(r))
        except Exception as e:
            return "Not a JSON", 400
    return "were", 200
