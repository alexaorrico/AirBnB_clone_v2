#!/usr/bin/python3
"""create a route /status on the object app_views that returns a JSON"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def show_create_states():
    """
    GET REQUEST: return json string containing all State objects in storage
    POST REQUEST: creates a new State from request and returns new object's dict in JSON string
    ERROR HANDLING: throws 400 error if 'name' key not in body response dict, or body response not
    a valid json
    """
    if request.method == 'GET':
        # retrieve a dictionary of all states in storage
        all_states_dict = storage.all(State)
        all_states_list = []
        # add each dictionary value (State object) to a list after calling to_dict() on it
        for state_obj in all_states_dict.values():
            all_states_list.append(state_obj.to_dict())
        return jsonify(all_states_list)

    else:
        if request.get_json():
            body = request.get_json()
            if 'name' in body:
                new_state = State(name=body['name'])
                new_state.save()
                return jsonify(new_state.to_dict()), 201
            else:
                abort(400, description="Missing name")
        else:
            abort(400, description="Not a JSON")


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def show_delete_update_state_from_id(state_id):
    """
    GET REQUEST: returns JSON string containing the state object with correspondong to state_id
    DELETE REQUEST: deletes a state object with corresponding state_id from storage and returns an emtpy dict
    PUT REQUEST: updates a state object with corresponding state_id from storage and returns a dict containing updated object
    ERROR HANDLING: throws a 404 error if state_id not found
    """
    all_states_dict = storage.all(State)

    for state_obj in all_states_dict.values():
        if state_obj.id == state_id:

            # return JSON string of object's dict representation
            if request.method == 'GET':
                return jsonify(state_obj.to_dict())

            # delete object from storage and return empty dict
            if request.method == 'DELETE':
                state_obj.delete()
                return {}

            # update object or throw 400 error if request body not a json
            # get http request body as dict
            body = request.get_json()
            updates_dict = {}
            if body:
                print(body)
                for k, v in body.items():
                    # check protected keys are not updated
                    if k not in ["id", "created_at", "updated_at"]:
                        # add unprotected keys and values to a new dict
                        updates_dict[k] = v
                # call update method of state_obj and pass in request body
                state_obj.__dict__.update(updates_dict)
                state_obj.save()
                return jsonify(state_obj.to_dict())
                    
            else:
                abort(400, description="Not a JSON")
            
            

    abort(404)
