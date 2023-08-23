#!/usr/bin/python3
import json
from flask import Response, jsonify, request, abort
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def getstate2():
    states = State.all()
    states_list = [state.to_dict() for state in states]
    return Response(json.dumps(states_list), mimetype='application/json')


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def getstate1(state_id):
    state = State.get(State, state_id)
    if state is None:
        abort(404)
    return Response(json.dumps(state.to_dict()), mimetype='application/json')


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def deletestate(state_id):
    state = State.get(State, state_id)
    if state is None:
        abort(404)
    return Response(json.dumps(state.to_dict()), mimetype='application/json')
