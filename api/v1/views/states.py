#!/usr/bin/python3
"""script to serve routes related to states objects"""
from models.state import State
from models import storage
from api.v1.views import app_views
import json

from flask import request

all_states = storage.all(State)  # is a dict
states = []
for key, value in all_states.items():
    states.append(value.to_dict())

@app_views.route('/states', methods=['GET'])
def serve_states():
    """Retrieves a list of all State objects"""
    return json.dumps(states)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def serve_state_id(state_id):
    """Retrives a State object"""
    # forming the key of the State instance -> State.id
    state_key = "State.{}".format(state_id)

    if state_key not in all_states.keys():
        return json.dumps({"error": "Not found"}), 404
    
    # use the get method that returns an instance based on Cls and id
    found_state = storage.get(State, state_id)
    return json.dumps(found_state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state_obj(state_id):
    """deletes a State object"""
    # forming the key of the State instance -> State.id
    state_key = "State.{}".format(state_id)

    if state_key not in all_states.keys():
        return json.dumps({"error": "Not found"}), 404
    
    state_to_delete = all_states[state_key] # gives us the instance
    storage.delete(state_to_delete)
    return json.dumps({}), 200


# @app_views.route('/states', methods=['POST'], strict_slashes=False)
# def create_new_state():
#     """creates a State"""

#     data_entered = request.get_json()
#     print("data is ", data_entered)
#     print("type is ", type(data_entered))
    # if data_entered is None:
    #     return "Not a JSON", 400
    
    # # if name not in dict
    # if data_entered.get('name') is None:
    #     return "Missing name", 400
#     storage.new(data_entered)
#     print("all states", storage.all(State))

    
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state_obj(state_id):
    """updates a State object"""
    # forming the key of the State instance -> State.id
    state_key = "State.{}".format(state_id)

    if state_key not in all_states.keys():
        return json.dumps({"error": "Not found"}), 404
    
    data_entered = request.get_json()  # method returns None if fails
    if data_entered is None:
        return "Not a JSON", 400
    
    state_to_update = all_states[state_key] # gives us the instance

    # UPDATE THIS. SHOULD CHECK ALL KEY,VALUES ENTERED IN THE POST
    # REQUEST DICT, THEN USE THAT TO UPDATE THE VALUES
    # NOT AS DONE BELOW (SHOULD BE DYNAMIC)
    state_to_update.name = data_entered['name']
    return json.dumps(state_to_update.to_dict()), 200
