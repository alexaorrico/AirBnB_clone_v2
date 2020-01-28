#!/usr/bin/python3
from models import storage
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route("/amenities",
                 methods=["GET"],
                 strict_slashes=False)
def get_all_amenities():
    """retrieves all amenities"""
    amenity_list = []
    amenities = storage.all("Amenity").values()
    for amenity in amenities:
        amenity_list.append(amenity.to_dict())
    return (jsonify(amenity_list))


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """get a single amenity"""
    amenity_obj = storage.get('Amenity', amenity_id)
    if amenity_obj is None:
        abort(404)
    else:
        return (jsonify(amenity_obj.to_dict()))


@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes a specific amenity based on id"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()
        return (jsonify({})), 200


@app_views.route("/amenities",
                 methods=["POST"],
                 strict_slashes=False)
def post_amenity():
    """create a new amenity"""
    if not request.get_json():
        return (jsonify({"error": "Not a JSON"})), 400
    if "name" not in request.get_json():
        return (jsonify({"error": "Missing name"})), 400
    json_dict = request.get_json()
    new_amenity = Amenity(**json_dict)
    new_amenity.save()
    return (jsonify(new_amenity.to_dict())), 201


@app_views.route("/amenities/<amenity_id>",
                 methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):

    ignore = ["id", "state_id", "created_at", "updated_at"]
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return (jsonify({"error": "Not a JSON"})), 400
    for k, v in request.get_json().items():
        if k not in ignore:
            setattr(amenity, k, v)
    storage.save()
    return (jsonify(amenity.to_dict())), 200
