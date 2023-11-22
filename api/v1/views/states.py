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
