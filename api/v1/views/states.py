#!/usr/bin/python3
"""
New view for State objects that handles taht handles all default ResFul API.
"""


from flask import abort
from flask import jsonify
from models.state import State
from models import storage
from flask import Flask
from api.v1.views import app_views
from flask import request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_task():
    """
    """
    state_list = []
    for state in storage.all('State').values():
        state_list.append(state.to_dict())
    return jsonify(state_list)


@app_views.route("/states/<string:state_id>", methods=['GET'],
                 strict_slashes=False)
def get_task_id(state_id):
    """
    Return id of the function
    """
    stateArr = storage.get("State", state_id)
    if stateArr is None:
        abort(404)
    return jsonify(stateArr.to_dict())


@app_views.route("states/<string:state_id>", methods=['DELETE'],
                 strict_slashes=False)
def get_task_delete(state_id):
    """
    method Delete of the function
    """
    stateArr = storage.get('State', state_id)
    if stateArr is None:
        abort(404)
    else:
        storage.delete(stateArr)
    return jsonify({}), 200


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def set_task_POST():
    """
    State object
    """
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400

    state_post = State(**request.get_json())
    state_post.save()
    return jsonify(state_post.to_dict()), 201


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
