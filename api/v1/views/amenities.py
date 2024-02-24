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


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def amenity_create():
  """
  Creates an amenity route
  :Return: newly created amenity object
  """
  am_json = request.get_json(silent=True)
  if am_json is None:
    abort(400, 'Not a JSON')
  if "name" not in am_json:
    abort(400, 'Missing name')
    
  new_am = Amenity(**am_json)
  new_am.save()
  resp = jsonify(new_am.to.json())
  resp.status_code = 201
  
  return resp


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
  """
  Get specific Amenity object by ID
  :param amenity_id: amenity obj id
  :Return: State object with the specific ID or error
  """

  fetched_obj = storage.get("Amenity", str(amenity_id))

  if fetched_obj is None:
    abort(404)

  return jsonify(fetched_obj.to_json())


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def amenity_put(amenity_id):
  """
  Updates specific Amenity objects by ID
  :param amenity_id: amenity object ID
  :Return: amenity obj and 200 on success, or 400 or 404 failure
  """
  am_json = request.get_json(silent=True)
  if am_json is None:
    abort(400, 'Not a JSON')
  fetched_obj = storage.get("Amenity", str(amenity_id))
  if fetched_obj is None:
    abort(400)
  for key, val in am_json.items():
    if key not in ["id", "created_at", "updated_at"]:
        setattr(fetched_obj, key,val)
    fetched_obj.save()
    return jsonify(fetched_obj.to_json())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def amenity_delete_by_id(amenity_id):
  """
  Deletes Amenity by ID
  :param amenity_id: Amenity obj id
  :Return: empty dict with a 200 or 404 if not found
  """

fetched_obj = storage.get("Amenity", str(amenity_id))

if fetched_obj is None:
  abort(404)

storage.delete(fetched_obj)
storage.save()

return jsonify({})
