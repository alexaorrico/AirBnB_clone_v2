#!/usr/bin/python3
"""Retrieving State objects"""

from models.state import State
from flask import request, jsonify
from models import storage
from api.v1.views import app_views

state_list = []
states = storage.all(State).values()
for state in states:
    state_list.append(state.to_dict())


@app_views.route('/states', methods=["GET", "POST"], strict_slashes=False)
def get_states():
    if request.method == 'GET':
        return jsonify(state_list)

    elif request.method == 'POST':
        name = request.get_json()
        if name.get('name') is None:
            return 'Missing name', 400
        try:
            value = name['name']
            new_dict = {
                '__class__': State.__name__,
                'created_at': State().created_at,
                'name': value,
                'id': State().id,
                'updated_at': State().updated_at
            }
            return new_dict, 201

        except Exception as e:
            return jsonify("Not a JSON"), 400
