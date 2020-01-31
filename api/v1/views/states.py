#!/usr/bin/python3
""" index file """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'])
def get_states():
    """ status function """
    my_list = []
    st = storage.all("State")
    for state in st.values():
        my_list.append(state.to_dict())
    return jsonify(my_list)


@app_views.route('/states/<string:state_id>', methods=['GET'])
def get_state(state_id):
    """get state by id"""
    try:
        return jsonify(storage.get("State", state_id).to_dict())
    except:
        abort(404)


@app_views.route('/states/<string:state_id>', methods=['DELETE'])
def delete_state(state_id):
    """delete state by id"""
    try:
        my_state = storage.get("State", state_id)
        my_state.delete()
        return {}, 200
    except:
        abort(404)


@app_views.route('/states', methods=['POST'])
def create_state():
    """creates a new state"""
    try:
        return {}, 200
    except:
        abort(404)
