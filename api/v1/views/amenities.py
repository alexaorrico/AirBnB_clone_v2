#!/usr/bin/python3
"""
Routes for handling Amenity objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def retrieve_all_amenities():
    """
    Retrieves all Amenity objects.

    :return: JSON of all amenities
    """
    amenity_list = []
    amenity_obj = storage.all("Amenity")
    for obj in amenity_obj.values():
        amenity_list.append(obj.to_json())

    return jsonify(amenity_list)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """
    Create an amenity.

    :return: Newly created amenity object
    """
    amenity_json = request.get_json(silent=True)
    if amenity_json is None:
        abort(400, 'Not a JSON')
    if "name" not in amenity_json:
        abort(400, 'Missing name')

    new_amenity = Amenity(**amenity_json)
    new_amenity.save()
    rsponce = jsonify(new_amenity.to_json())
    rsponce.status_code = 201

    return rsponce


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """
    Get a specific Amenity object by ID.

    :param amenity_id: The ID of the amenity object
    :return: Amenity object with the specified ID or error
    """

    obj_fetched = storage.get("Amenity", str(amenity_id))

    if obj_fetched is None:
        abort(404)

    return jsonify(obj_fetched.to_json())


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity_by_id(amenity_id):
    """
    Update a specific Amenity object by ID.

    :param amenity_id: The ID of the amenity object
    :return: Amenity object and 200 on success, or 400 or 404 on failure
    """
    amenity_json = request.get_json(silent=True)
    if amenity_json is None:
        abort(400, 'Not a JSON')
    obj_fetched = storage.get("Amenity", str(amenity_id))
    if obj_fetched is None:
        abort(404)
    for key, val in amenity_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(obj_fetched, key, val)
    obj_fetched.save()
    return jsonify(obj_fetched.to_json())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """
    Delete an Amenity by ID.

    :param amenity_id: The ID of the amenity object
    :return: Empty dictionary with 200 or 404 if not found
    """

    obj_fetched = storage.get("Amenity", str(amenity_id))

    if obj_fetched is None:
        abort(404)

    storage.delete(obj_fetched)
    storage.save()

    return jsonify({})
