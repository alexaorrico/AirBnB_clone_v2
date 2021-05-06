#!/usr/bin/python3
""" Your first endpoint (route) will be to return the status of your API """
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
import json

@app_views.route('/states/', methods=['GET',])
def show_states():
    lista = []
    states = storage.all(State).values()
    for state in states:
        lista.append(state.to_dict())
    return jsonify(lista)

@app_views.route('states/<state_id>', methods=['GET',])
def show_state(state_id):
    states = storage.all(State).values()
    for state in states:
        return state.id + "\n"
        if state.id == state_id:
            return state.id
    