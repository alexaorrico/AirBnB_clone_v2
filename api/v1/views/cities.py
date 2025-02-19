#!/usr/bin/python3
"""
Route for handling state objects and operations
"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import City

@app_views.route("/states/<state_id>/cities", methods=["GET"],
        strict_slashes=False)
def city_by_state(state_id):
    """
    Retrieves all citty objects
    :return JSON list of all cities
    """
    city_list = []
    state_obj = storage.get("State", state_id)
    if state_obj is None:
        abort(404)

    for obj in state_obj.cities:
        city_list.append(obj.to_dict())
    return jsonify(city_list)

@app_views.route("/states/<state_id>/cities", methods=["POST"],
        strict_slashes=False)
def city_create(state_id):
    """
    Create a new City object
    
    :return: JSON of the newly created object
    """
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')
    if storage.get("State", str(state_id)) is None:
        abort(404)

    if 'name' not in city_json:
        abort(400, 'Missing name')

    city_json["state_id"] = state_id

    # create a new state object using the JSON data
    new_city = City(**city_json)
    new_city.save()

    # Return the new state object as JSON with 202 status code
    resp = jsonify(new_city.to_dict())
    resp.status_code = 201

    return resp

@app_views.route("/cities/<city_id>", methods=["GET"],
                strict_slashes=False)
def city_by_id(city_id):
    """
    Retrieve specific city object by ID
    :param state_id: city object ID
    :return: JSON of the state objects with the specific id or 404 error

    """
    # Fetch the city objects by ID
    fetched_obj = storage.get("City", str(city_id))
    # if the object is not found return 404 error
    if fetched_obj is None:
        abort(404)

    # Return the state object as JSON
    return jsonify(fetched_obj.to_dict())

@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def city_put(city_id):
    """
    Update a specific city object by ID
    :param state_id: state objects ID
    :return: JSON of the updated state object and 200 on success
    or 400 0r 404 on failure
    """
    # Get the JSON request body
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')
    fetched_obj = storage.get("City", str(city_id))
    if fetched_obj is None:
        abort(404)
    # update the state object with new values , ignoring certain keys
    for key, val in city_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    # Return the updated state object as JSON
    return jsonify(fetched_obj.to_dict())

@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def city_delete_by_id(city_id):
    """
    Delete a City object by ID
    :param state_id: city object ID
    :return Empty dictionary with 200 status code or 404 if not found

    """
    # Fetch the state object by ID
    fetched_obj = storage.get("City", str(city_id))
    if fetched_obj is None:
        abort(404)

    # Delete the city object
    storage.delete(fetched_obj)
    storage.save()

    # Return an empty dictionary with a 200 status code
    return jsonify({})

