#!/usr/bin/python3

"""
a new view for Amenity objects that handles all default RESTFul API actions
"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def retrieve_amenity():
    """
    Retrieves all the amenities
    """

    amenity_list = []
    amenities = storage.all(Amenity)
    for amenity in amenities.values():
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def retrieve_amenity_using_amenityid(amenity_id):
    """
    REtrieves the state using the amenity id
    Raises a 404 error if the amenity_id isnt linked to a amenity
    """

    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity_using_amenityid(amenity_id):
    """
    Deletes a state using the amenity id
    Raises a 404 error If the amenity_id is not linked to any Amenity object
    Returns an empty dictionary with the status code 200
    """

    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        amenity.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def post_amenity():
    """
    Posts a new Amenity
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    amenity_data = request.get_json()
    amenity = Amenity()
    for key, value in amenity_data.items():
        setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_ameity(amenity_id):
    """
    Updates a amenity using the amenity id
    Returns a 404 error if the amenity id is not linked to any amenity
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    amenity = storage.get(Amenity, amenity_id)
    keys_ignore = ["id", "updated_at", "created_at"]
    if amenity:
        for key, value in request.get_json().items():
            if key not in keys_ignore:
                setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200
    abort(404)
