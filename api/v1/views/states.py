#!/usr/bin/python3
""" index file """

from api.v1.views import app_views
from flask import jsonify
from models.state import State


@app_views.route('/states')
def states():
    """ status function """
    return jsonify(storage.all("State"))


@app_views.route('/states/<string:state_id>', methods=['GET'])
def get_state():
    """"""
    return jsonify(storage.get("State", state_id))
