#!/usr/bin/python3
"""
a new view for State objects that handles all default RESTFul API actions
"""
from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    all_amenities = storage.all("Amenity").values()
    result = [amenity.to_dict() for amenity in all_amenities]
    return jsonify(result), 200


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves an amenity object"""
    amenity = storage.get("Amenity", str(amenity_id))
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict()), 200


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an Amenity object"""
    amenity = storage.get("Amenity", str(amenity_id))
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return ({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Creates an Amenity"""
    amenity_dict = request.get_json(silent=True)
    if amenity_dict is None:
        abort(400, "Not a JSON")
    if "name" not in amenity_dict:
        abort(400, "Missing name")

    amenity_inst = Amenity(**amenity_dict)
    amenity_inst.save()
    return jsonify(amenity_inst.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an Amenity object"""
    amenity_obj = storage.get("Amenity", str(amenity_id))
    amenity_dict = request.get_json(silent=True)
    if amenity_obj is None:
        abort(404)
    if amenity_dict is None:
        abort(400, "Not a JSON")
    for key, val in amenity_dict.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity_obj, key, val)
    amenity_obj.save()
    return jsonify(amenity_obj.to_dict()), 200


# get the object to be updated by it's id
# get the dictionary repr of state instance for id=state_id using get_json()
# check if it's a valid json and return none if it's not
# iterate the dictionary
# id, created_at and updated_at should not be available to be set
# set object attributes based on their keys
