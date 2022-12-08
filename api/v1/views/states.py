#!/usr/bin/python3
"""
New view for class State
To handle all default Restful API actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'])
def list_all_states():
    """Returns the list of all `State` objects"""
    list_states = [obj.to_dict() for obj in storage.all('State').values()]
    return jsonify(list_states)


# @app_views.route('/states/<state_id>', methods=['GET'])
# def pick_state_obj(state_id):
#     """Retrieves a `State` object/Error if no linkage to any id"""
#     state_pick = storage.get("State", state_id)
#     if state_pick is None:
#         # use abort to return 404
#         # in the middle of a route
#         abort(404)
#     return jsonify(state_pick.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """
    Deletes a `State`object based on its id
    Raise error if no linkage found
    """
    state_rm = storage.get("State", state_id)
    if state_rm is None:
        abort(404)
    state_rm.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'])
def post_state():
    """Method to create a `State` object"""
    json_data = request.get_json()
    if not json_data:
        abort(400, 'This is not JASON!!')
    elif 'name' not in json_data:
        abort(400, 'Missing name')
    new_post = State(name=json_data['name'])
    new_post.save()
    return jsonify(new_post.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def upd_state(state_id):
    """
    Update a `State` object
    Error if no linkage found
    """
    json_data = request.get_json()
    if not json_data:
        abort(400, 'This is not JASON!!')

    state_upd = storage.get("State", state_id)
    if state_upd is None:
        abort(404)
    state_upd.name = json_data['name']
    state_upd.save()
    return jsonify(state_upd.to_dict()), 200
