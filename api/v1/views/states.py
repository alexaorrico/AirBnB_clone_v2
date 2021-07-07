#!/usr/bin/python3
""" State file """

from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
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
    payload = request.get_json()
    if payload is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    else:
        if 'name' in payload:
            new_state = State(name=payload.get('name'))
            new_state.save()
            return jsonify(new_state.to_dict()), 200
        else:
            return make_response(jsonify({"error": "Missing name"}), 400)


@app_views.route('/states/<string:state_id>', methods=['PUT'])
def update_state(state_id):
    """ updates a state instance """

    update = request.get_json()
    if update is None:
        abort(400, "Not a JSON")
    updated_state = storage.get("State", id=state_id)
    setattr(updated_state, 'name', update.get('name'))
    updated_state.save()
    return (updated_state.to_dict())
