#!/usr/bin/python3
""" states view class """
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/states/', methods=["GET"])
@app_views.route('/states/<state_id>', methods=["GET", "DELETE"])
def get_state_id(state_id=None):
    """ get certian state"""
    states = storage.all("State")
    if state_id == None:
        return jsonify([obj.to_dict() for obj in states.values()])
    state = None
    for obj in states.values():
        if getattr(obj, "id") == state_id:
            state = obj.to_dict()
    if state == None:
        abort(404)
    return jsonify(state)
