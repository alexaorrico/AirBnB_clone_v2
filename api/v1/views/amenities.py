#!/usr/bin/python3
"""
Route for handling Amenity objects and operations
"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.amenity import Amenity

@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenity_get_all():
    """
    Retrieves all Amenity objects
    :return JSON list of all states
    """
    amenity_list = []
    amenity_obj = storage.all("Amenity")
    for obj in amenity_obj.values():
        amenity_list.append(obj.to_dict())

    return jsonify(amenity_list)

@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def amenity_create():
    """
    Create a new amenity object
    
    :return: JSON of the newly created object
    """
    amenity_json = request.get_json(silent=True)
    if amenity_json is None:
        abort(400, 'Not a JSON')
    if 'name' not in amenity_json:
        abort(400, 'Missing name')

    # create a new state object using the JSON data
    new_amenity = Amenity(**amenity_json)
    new_amenity.save()

    # Return the new state object as JSON with 202 status code
    resp = jsonify(new_amenity.to_dict())
    resp.status_code = 201

    return resp

@app_views.route("/amenities/<amenity_id>", methods=["GET"], strict_slashes=False)
def amenity_by_id(amenity_id):
    """
    Retrieve specific amenity object by ID
    :param amenity_id: amenity object ID
    :return: JSON of the amenity objects with the specific id or 404 error

    """
    # Fetch the state objects by ID
    fetched_obj = storage.get("Amenity", str(amenity_id))
    # if the object is not found return 404 error
    if fetched_obj is None:
        abort(404)

    # Return the state object as JSON
    return jsonify(fetched_obj.to_dict())

@app_views.route("/amenities/<amenity_id>", methods=["PUT"], strict_slashes=False)
def amenity_put(amenity_id):
    """
    Update a specific Amenity object by ID
    :param amenity_id: amenity object ID
    :return: JSON of the updated amenity object and 200 on success
    or 400 0r 404 on failure
    """
    # Get the JSON request body
    amenity_json = request.get_json(silent=True)
    if amenity_json is None:
        abort(400, 'Not a JSON')
    fetched_obj = storage.get("Amenity", str(amenity_id))
    if fetched_obj is None:
        abort(404)
    # update the state object with new values , ignoring certain keys
    for key, val in amenity_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    # Return the updated state object as JSON
    return jsonify(fetched_obj.to_dict())

@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
        strict_slashes=False)
def amenity_delete_by_id(amenity_id):
    """
    Delete a amenity object by ID
    :param amenity_id: amenity object ID
    :return Empty dictionary with 200 status code or 404 if not found

    """
    # Fetch the state object by ID
    fetched_obj = storage.get("Amenity", str(amenity_id))

    if fetched_obj is None:
        abort(404)

    # Delete the state object
    storage.delete(fetched_obj)
    storage.save()

    # Return an empty dictionary with a 200 status code
    return jsonify({})
