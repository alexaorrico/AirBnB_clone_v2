#!/usr/bin/python3

from flask import Flask, request, jsonify
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def states_list():
    state_objects = storage.all(State)
    state_list = []
    for key, val in state_objects.items():
        state_list.append(val.to_dict())
    return jsonify(state_list)
