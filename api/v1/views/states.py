#!/usr/bin/python3
""" State view """

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def list_states():
    """ Lists all State objects """
    all_states = storage.all('State')
    return jsonify([state.to_dict() for state in all_states.values()])
