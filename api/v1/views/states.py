#!/usr/bin/python3
""" tbc """
import json
from flask import Flask, request, jsonify, abort
from models.state import State
from models import storage
from api.v1.views import app_views
from werkzeug.exceptions import HTTPException

app = Flask(__name__)


@app_views.route('/states/', methods=['GET'])
def get_all_states():
    """ tbc """
    state_list = []
    states_dict = storage.all(State)
    for item in states_dict:
        state_list.append(states_dict[item].to_dict())
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_one_states(state_id):
    """ tbc """
    states_dict = storage.all(State)
    for item in states_dict:
        if states_dict[item].to_dict()['id'] == state_id:
            return jsonify(states_dict[item].to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_one_states(state_id):
    """ tbc """
    the_state = storage.get(State, state_id)
    if the_state is not None:
        storage.delete(the_state)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/', methods=['POST'])
def post_state():
    """ tbc """
    content = request.headers.get('Content-type')
    if content != 'application/json':
        abort(400, description='Not a JSON')
    json_dict = request.json
    if 'name' not in json_dict:
        abort(400, description='Missing name')
    new_state = State()
    for item in json_dict:
        setattr(new_state, item, json_dict[item])
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def put_state_attribute(state_id):
    """ tbc """
    the_state = storage.get(State, state_id)
    if the_state is None:
        abort(404)
    content = request.headers.get('Content-type')
    if content != 'application/json':
        abort(400, description='Not a JSON')
    j = request.json
    for i in j:
        if j[i] != 'id' and j[i] != 'created_at' != j[i] != 'updated_at':
            setattr(the_state, i, j[i])
    storage.save()
    return jsonify(the_state.to_dict()), 200
