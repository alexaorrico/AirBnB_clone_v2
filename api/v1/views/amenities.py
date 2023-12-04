#!/usr/bin/python3
''' Serve amenities '''

from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False, methods=['GET'])
@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=['GET'])
def get_amenities(amenity_id=None):
    """
    Returns state objects based on path

    with amenity_id: Returns a single object
    without amenity_id: Returns every state
    """
    new_list = []
    key = "Amenity." + str(amenity_id)
    if amenity_id is None:
        objs = storage.all(Amenity)
        for key, value in objs.items():
            new_list.append(value.to_dict())
    elif key in storage.all(Amenity).keys():
        return jsonify(storage.all(Amenity)[key].to_dict())
    else:
        abort(404)
    return jsonify(new_list)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id=None):
    """
    Deletes an amenity from the database
    """
    state = storage.get(Amenity, amenity_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities/", strict_slashes=False, methods=['POST'])
def post_amenities():
    """
    Post an amenity
    """
    if request.get_json() is None:
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    amenity = Amenity(**request.get_json())
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["PUT"])
def update_amenity(amenity_id=None):
    """ Update a state object
    """
    key = "Amenity." + str(amenity_id)
    if key not in storage.all(Amenity).keys():
        abort(404)
    if request.get_json() is None:
        abort(400, "Not a JSON")

    amenity = storage.get(Amenity, amenity_id)
    for key, value in request.get_json().items():
        if key not in ["created_at", "updated_at", "id"]:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
