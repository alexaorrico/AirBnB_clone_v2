#!/usr/bin/python3
"""
File that configures the routes of state
"""
from api.v1.views import app_views
from flask import jsonify
from models.state import State
from models import storage


@app_views.route("/states", strict_slashes=False)
@app_views.route("/states/<state_id>", strict_slashes=False)
def get_state(state_id=None):
    """
    Route to get states
    """
    print(state_id)
    list_obj = []
    if not state_id:
        for val in storage.all().values():
            list_obj.append(val.to_dict())

        return jsonify(list_obj)

    return jsonify(storage.get("State", state_id).to_dict())
