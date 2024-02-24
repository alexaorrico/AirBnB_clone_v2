#!/usr/bin/python3
"""
Route for handling Amenity objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.ameity iport Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenity_get_all():
  """
  Retrives all Amenities objects
  :Returns: json of all states.
  """
  am_list = []
  am_obj = storage.all("Amenity")
  for obj in am_obj.values():
    am_list.append(obj.to_json())
    
  return jsonify(am_list)


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenity_create():
  """
  Creates an amenity route
  :Return: newly created amenity object
  """
  am+json = request.get_json(silent=True)
