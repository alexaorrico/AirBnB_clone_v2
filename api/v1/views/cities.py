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


@app_views.route("states/<state_id>/cities", methods=["POST"],
                strict_slashes=FALSE)
def city_by_state(state_id):
    """
    Create city route
    param: state_id - state id
    :Returns: newly created obj
    """
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')

    if not storage.get("State", str(state_id)):
        abort(404)

    if "name" not in city_json:
        abort(400, 'Missing name')

  city_json["state_id"] = state_id

  new_city City(**city_json)
  new_city.save()
  resp = jsonify(new_city.to_json())
  resp.status_code = 201

  return resp


  @app_views.route("cities/<city_id>", methods=["GET"],
                    strict_slashes=False)
  def city_by_id(city_id):
      """
      Gets specific City object by ID
      :param city_id: city object id
      :Returns: city obj with the specified id or error
      """

      fetched_obj = storage.get("City", str(city_id))

      if fetched_obj is None:
          abort(404)

      return jsonify(fetched_obj.to_json())


@app_views.route("cities/<city_id>", methods=["PUT"], strict_slashes=False)
def city_put(city_id):
    """
    Updates specific city object ID
    :param city_id: city object ID
    :Returns: city object and 200 on success, or 400 or 404 in failure
    """
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')
    fetched_obj = storage.get("City", str(city_id))
    if fetched_obj is None:
        abort(404)
    for key, val in city_json.item():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    return jsonify(fetched_obj.to_json())


@app_views.route("cities/<city_id>", methods=["DELETE"],
                  strict_slashes=False)
def city_delete_by_id(city_id):
    """
    Deletes City by ID
    :param city_id: city object ID
    :Returns: Empty dict with 200 or 404 not found
    """

    fetched_obj = storage.get("City", str(city_id))

    if fetched_obj is None:
        abort(404)

    storage.delete(fetched_obj)
    storage.save()

    return jsonify({})
