#!/usr/bin/python3
"""
Route for handling state objects and operations
"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User

@app_views.route("/users", methods=["GET"], strict_slashes=False)
def user_get_all():
    """
    Retrieves all user objects
    :return JSON list of all states
    """
    user_list = []
    user_obj = storage.all("Users")
    for obj in user_obj.values():
        user_list.append(obj.to_dict())
    return jsonify(user_list)

@app_views.route("/users", methods=["POST"], strict_slashes=False)
def user_create():
    """
    Create a new user object
    
    :return: JSON of the newly created object
    """
    user_json = request.get_json(silent=True)
    if user_json is None:
        abort(400, 'Not a JSON')
    if "email" not in user_json:
        abort(400, "Missing email")
    if 'password' not in user_json:
        abort(400, 'Missing password')

    # create a new state object using the JSON data
    new_user = User(**user_json)
    new_user.save()

    # Return the new state object as JSON with 202 status code
    resp = jsonify(new_user.to_dict())
    resp.status_code = 201

    return resp

@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def user_by_id(user_id):
    """
    Retrieve specific user object by ID
    :param user_id: user object ID
    :return: JSON of the state objects with the specific id or 404 error

    """
    # Fetch the state objects by ID
    fetched_obj = storage.get("User", str(user_id))
    # if the object is not found return 404 error
    if fetched_obj is None:
        abort(404)

    # Return the state object as JSON
    return jsonify(fetched_obj.to_dict())

@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def user_put(user_id):
    """
    Update a specific user object by ID
    :param state_id: state objects ID
    :return: JSON of the updated user object and 200 on success
    or 400 0r 404 on failure
    """
    # Get the JSON request body
    user_json = request.get_json(silent=True)
    if user_json is None:
        abort(400, 'Not a JSON')
    fetched_obj = storage.get("User", str(user_id))
    if fetched_obj is None:
        abort(404)
    # update the user object with new values , ignoring certain keys
    for key, val in user_json.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    # Return the updated state object as JSON
    return jsonify(fetched_obj.to_dict())

@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def user_delete_by_id(user_id):
    """
    Delete a user object by ID
    :param user_id: user object ID
    :return Empty dictionary with 200 status code or 404 if not found

    """
    # Fetch the state object by ID
    fetched_obj = storage.get("User", str(user_id))
    if fetched_obj is None:
        abort(404)

    # Delete the state object
    storage.delete(fetched_obj)
    storage.save()

    # Return an empty dictionary with a 200 status code
    return jsonify({})

