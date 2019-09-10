#!/usr/bin/python3
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.state import State


@app_views.route('/states/', methods=['GET'])
def list_all_states():
    data = storage.all(State)
    new = [val.to_dict() for key, val in data.items()]
    return jsonify(new)

@app_views.route('/states/<state_id>', methods=['GET'])
def specific_state(state_id=None):
    ''' returns an individual state object '''
    obj = storage.get(State, state_id)
    obj = obj.to_dict()
    return jsonify(obj)
