"""Module to create a new view for State objects"""
from flask import jsonify, Flask
from models import storage
from api.v1.views import app_views

@app_views.route('/states', methods=['GET'], strict_slashes = False)
def get_states():
    """Retrieves the list of all State objects"""
    all_states = storage.all('State')
    my_list = []
    for value in all_states.values():
        my_list.append(value.to_dict())
    return jsonify(my_list)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes = False)
def get_state_by_id(state_id):
    """Retrieves the state by ID"""
    state = storage.get('State', str(state_id))
    if state is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes = False)
def delete_state_by_id(state_id):
    """Deletes a state by ID"""
    state = storage.get('State', state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

# @app_views.route('/api/v1/states', methods=['POST'])
