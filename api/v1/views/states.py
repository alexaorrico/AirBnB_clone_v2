#!/usr/bin/python3
""" tbc """
import json
from flask import Flask, request, jsonify
from models.state import State
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

@app_views.route('/states/', methods=['GET'])
def get_all_states():
    """ tbc """
    state_list = []
    states_dict = storage.all(State)
    for item in states_dict:
        state_list.append(states_dict[item].to_dict())
    return jsonify(state_list)
