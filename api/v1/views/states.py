#!/usr/bin/python3
"""a blueprint module that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State


@app_views.route('/states')
def all_states():
    return jsonify([state.to_dict()
                   for state in storage.all(State).values()])
