#!/usr/bin/python3
"""
Routes for handling places objects and operations.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def places_by_city(city_id):
  """
  Retrieves all place objects by city
  :return: json of all places
  """
  place_list = []
  city_obj = storage.get("City", str(city_id))
  for obj in city_obj.places:
    place_list.append(obj.to_json())

  return jsonify(place_list)
