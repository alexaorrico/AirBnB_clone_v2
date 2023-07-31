#!/usr/bin/python3

from flask import Flask, jsonify, request
from models.state import State
from models import storage


all_state = storage.all(State)
states = []
for state in all_state.values():
    _dict = state.to_dict()
    states.append(_dict)

app = Flask(__name__)


@app.route('/api/v1/states', methods=['GET', 'POST'],
           strict_slashes=False)
def list_states():
    """retrieves all State Objects or Post http body request"""
    if request.method == 'GET':
        return jsonify(states)
    elif request.method == 'POST':
        try:
            """extract the data passed and checks if it is
            a valid JSON data"""
            data = request.get_json()
            if data.get('name'):
                """Now, checks if name is not missing"""
                new_state = State(**data).to_dict()
                states.append(new_state)
                return jsonify(new_state), 201
            return jsonify(error="Missing name"), 400

        except Exception as e:
            return jsonify(error="Not a JSON"), 400


@app.route('/api/v1/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
           strict_slashes=False)
def state_id(state_id):
    """retrieves or deletes a State Object using its Id"""
    for state in states:
        if state["id"] == state_id:
            if request.method == 'GET':
                return jsonify(state), 200
            elif request.method == 'DELETE':
                states.remove(state)
                return jsonify({}), 200
            elif request.method == 'PUT':
                try:
                    """extract the data passed and checks if it is
                    a valid JSON data"""
                    data = request.get_json()
                    ignore_keys = ['id', 'created_at', 'updated_at']
                    new_data = {key: value for key, value in data.items()
                                if key not in ignore_keys}
                    state.update(new_data)
                    return jsonify(state), 200

                except Exception as e:
                    return jsonify(error=e), 400

    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
