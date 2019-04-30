from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.state import State
"""Routing for AirBnB state object"""


dic = storage.all(State)
@app_views.route('/states/<state_id>', methods=['GET'])
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    if request.method == 'GET':
        if state_id is None:
            states_list = []
            for key, value in dic.items():
                states_list.append(value.to_dict())
            return jsonify(states_list)
        else:
            for key, value in dic.items():
                if value.id == state_id:
                    return jsonify(value.to_dict())
            abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id=None):
    if request.method == 'DELETE':
        empty = {}
        if state_id is None:
            abort(404)
        for key, value in dic.items():
            if value.id == state_id:
               storage.delete(value)
            return jsonify(empty), 200
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    flag = 0
    if not request.json:
        abort(400, 'Not a JSON')
    body = request.get_json()
    for key in body:
        if key == 'name':
            flag = 1
    if flag == 0:
        abort(400, "Missing name")
    new_state = State(body)
    new_state_dic = new_state.to_dict()
    return jsonify(new_state_dic), 201
