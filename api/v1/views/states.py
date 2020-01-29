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

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_task():
    """
    """
    state_list = []
    for state in storage.all('State').values():
        state_list.append(state.to_dict())
    return jsonify(state_list)


@app_views.route("/states/<string:state_id>",methods=['GET'], strict_slashes=False)
def get_task_id(state_id):
    """
    Return id of the function
    """
    stateArr = storage.get("State", state_id)
    if stateArr is None:
        abort(404)
    return jsonify(stateArr.to_dict())


@app_views.route("states/<string:state_id>", methods=['DELETE'], strict_slashes=False)
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


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
