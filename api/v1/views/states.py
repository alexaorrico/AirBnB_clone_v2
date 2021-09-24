#!/usr/bin/python3

from os import abort
from flask import Flask, jsonify, request, make_response
from api.v1.views import app_views
from models import storage
app = Flask(__name__)


@app_views.route('/states', methods=['GET'])
def getAll_states():
    """get all states"""
    states = []
    all = storage.all("State").values()
    for sts in all:
        states.append(sts.to_dict())
    return jsonify(states)


@app_views.route('/states/<string:state_id>', methods=['GET'])
def getById(state_id):
    """get state by state_id"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'])
def deleteById(state_id):
    """ delete by id"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/<string:state_id>', methods=['PUT'])
def update_state(state_id):
    """"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    data = request.get_json()

    state.name = data['name']
    state.save()
    return jsonify(state.to_dict()), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', threaded=True)
