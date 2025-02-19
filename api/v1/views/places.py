#!/usr/bin/python3
"""
Route for handling state objects and operations
"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.place import Place

@app_views.route("/cities/<city_id>/places", methods=["GET"],
        strict_slashes=False)
def place_by_city(city_id):
    """
    Retrieves all place objects
    :return JSON list of all cities
    """
    place_list = []
    city_obj = storage.get("City", str(city_id))
    for obj in city_obj.places:
        place_list.append(obj.to_dict())
    return jsonify(place_list)

@app_views.route("/cities/<city_id>/places", methods=["POST"],
        strict_slashes=False)
def place_create(state_id):
    """
    Create a new place object
    
    :return: JSON of the newly created object
    """
    place_json = request.get_json(silent=True)
    if place_json is None:
        abort(400, 'Not a JSON')
    if not storage.get("User", place_json["user_id"]):
        abort(404)
    if not storage.get("City", city_id):
        abort(404)
    if "user_id" not in place_json:
        abort(400, "Missing user_id")
    if 'name' not in place_json:
        abort(400, 'Missing name')

    place_json["city_id"] = city_id

    # create a new place object using the JSON data
    new_place = Place(**place_json)
    new_place.save()

    # Return the new state object as JSON with 202 status code
    resp = jsonify(new_place.to_dict())
    resp.status_code = 201

    return resp

@app_views.route("/places/<place_id>", methods=["GET"],
                strict_slashes=False)
def place_by_id(place_id):
    """
    Retrieve specific place object by ID
    :param state_id: place object ID
    :return: JSON of the place objects with the specific id or 404 error

    """
    # Fetch the place objects by ID
    fetched_obj = storage.get("Place", str(place_id))
    # if the object is not found return 404 error
    if fetched_obj is None:
        abort(404)

    # Return the state object as JSON
    return jsonify(fetched_obj.to_dict())

@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def place_put(place_id):
    """
    Update a specific place object by ID
    :param state_id: place objects ID
    :return: JSON of the updated place object and 200 on success
    or 400 0r 404 on failure
    """
    # Get the JSON request body
    place_json = request.get_json(silent=True)
    if place_json is None:
        abort(400, 'Not a JSON')
    fetched_obj = storage.get("Place", str(place_id))
    if fetched_obj is None:
        abort(404)
    # update the place object with new values , ignoring certain keys
    for key, val in place_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    # Return the updated place object as JSON
    return jsonify(fetched_obj.to_dict())

@app_views.route("/places/<place_id>", methods=["DELETE"],
        strict_slashes=False)
def place_delete_by_id(place_id):
    """
    Delete a place object by ID
    :param place_id: city object ID
    :return Empty dictionary with 200 status code or 404 if not found

    """
    # Fetch the state object by ID
    fetched_obj = storage.get("Place", str(place_id))
    if fetched_obj is None:
        abort(404)

    # Delete the city object
    storage.delete(fetched_obj)
    storage.save()

    # Return an empty dictionary with a 200 status code
    return jsonify({})

