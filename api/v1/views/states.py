#!/usr/bin/python3
""" Handles all State requests for the API """

from api.v1.views import app_views
from flask import jsonify
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'])
def all(state):
    """ Returns a JSON of State objects """
    states = []
    for obj in storage.all(State).values():
        states.append(obj.to_dict())
    return jsonify(states)

