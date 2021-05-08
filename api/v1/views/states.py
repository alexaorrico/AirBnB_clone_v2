#!/usr/bin/python3

"""
Create a new view for State objects that handles
all default RestFul API actions.
"""

from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get():
    """Retrieve all state objects"""
    l = [obj.to_dict() for obj in storage.all("State").values()]
    return jsonify(l)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_by_id(state_id):
    """Retrieve a state object by id"""
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())
