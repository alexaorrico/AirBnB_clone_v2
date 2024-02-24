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


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def place_create(city_id):
  """
  Creates a place route
  :return: Newly created place object
  """
  place_json = request.get_json(silent=True)
  if place_json is None:
    abort(400, 'Not a JSON')
  if not storage.get("User", place_json["user_id"]):
    abort(404)
  if not storage.get("City", city_id):
    abort(404)
  if "user_id" not in place_json:
    abort(400, 'Missing user_id')
  if "name" not in place_json:
    abort(400, 'Missing name')

  place_json["city_id"] = city_id

  new_place = Place(**place_json)
  new_place.save()
  resp = jsonify(new_place.to.json())
  resp.status_code = 201

  return resp


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def place_by_id(place_id):
  """
  Get a specific Place obect by id
  :param place_id: place obj id
  :Return: place obj with specified id or error
  """

  fetched_obj = storage.get("Place", str(place_id))

  if fetched_obj is None:
    abort(404)

  return jsonify(fetched_obj.to_json())


@app_views.route("/cities/<city_id>/places", methods=["PUT"],
                 strict_slashes=False)
def place_put(place_id):
  """
  Updates specific Place obj by id
  :param place_id: place obj id
  :Return: Place obj and 200 on success, or 400or 404 on error
  """
  place_json = request.get.json(silent=True)

  if place_json is None:
    abort(400, 'Not a JSON')

  fetched_obj = storage.get("Place", str(place_id))

  if fetched_obj is None:
    abort(404)

  for key, val in place_json.items():
    if key not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
      setattr(fetched_obj, key, val)

  fetched_obj.save()

  return jsonify(fetched_obj.to_json())


@app_views.route("/cities/<city_id>/places", methods=["DELETE"],
                 strict_slashes=False)
def place_delete_by_id(place_id):
  """
  Deletes Place by ID
  :param place_id: Place obj ID
  :Return: empty dict with 200 or 404 if not found
  """

  fetched_obj = storage.get("Place", str(place_id))

  if fetched_obj is None:
    abort(404)

  storage.delete(fetched_obj)
  storage.save()

  return jsonify({})
