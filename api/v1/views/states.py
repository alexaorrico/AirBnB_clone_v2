#!/usr/bin/python3
"""view states object"""


from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify


@app_views.route('/states', strict_slashes=False)
def states():
    """return list of all objects State"""
    new_list = list()
    lst_states = storage.all('State')
    for value in lst_states.values():
        new_list.append(value.to_dict())
    return jsonify(new_list)
