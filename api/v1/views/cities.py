#!/usr/bin/python3
"""
Routes for handling state objects and operations.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def city_by_state(state_id):
  """
  Retrieves all city objects from specific states
  :Returns: json of all cities in a state or 404 error
  """
  city_list = []
  state_obj = storage.get("State", state_id)
  
  if state_obj is None:
    abort(404)
  for obj in state_obj.cities:
    city_list.append(obj.to_json())
    
  return jsonify(city_list)

@app_views.route("states/<state_id>/cities", methods=["POST"]
                strict_slashes=FALSE)
def city_by_state(state_id):
    """
    Create city route
    param: state_id - state id
    :return: newly created obj
    """
    city_json = request.get_json(silent=True)
    
