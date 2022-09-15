#!/usr/bin/python3
"""view states object"""

from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify


@app_views.route('/states', strict_slashes=False)
def states():
    """return list of all objects State"""
    new_list = list()
    for value in storage.all('State').values():
        new_list.append(value.to_dict())
    return jsonify(new_list)

@app_views.route('/states/<state_id>', strict_slashes=False)
def states_id(state_id=None):
    """Return dictionary of specific state"""
    return storage.get("State", state_id)
