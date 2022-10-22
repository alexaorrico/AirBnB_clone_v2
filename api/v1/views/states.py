#!/usr/bin/python3
""" New view for states object that handles all
default RESTFul API actions. """

from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State

@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def fetch_states():
  """ Retrieves the list of all State objects. """
  if request.method = 'GET':
    all_states = storage.all(State).values()
    list_states = []

    for state in all_states:
      list_states.append(state.to_dict())
    return jsonify(list_states)
  
  if request.method = 'POST':
    req_data = request.get_json()
    if not req_data:
      abort(400, description="Not a JSON")
      
    if "name" not in req_data:
      abort(400, description="Missing name")
      
    state = (**req_data)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)

@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def fetch_state_id(state_id=None):
  """ Retrieves a State object given its id.
  Returns 404 error if id is not found.
  """
  state = storage.get(State, state_id)
  if not state:
    abort(404)
    
  if request.method = 'GET':
    return jsonify(state.to_dict())
  
  if request.method = 'DELETE':
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)
  
  if request.method = 'PUT':
    req_data = request.get_json()
    if not req_data:
      abort(400, description='Not a JSON')
    
    ignore_keys = ['id', 'created_at', 'updated_at']
    
    for key, value in req_data.items():
      if key not in ignore_keys:
        setatrr(state, key, value)
    storage.save()    
    return make_response(jsonify(state.to_dict()), 200)
