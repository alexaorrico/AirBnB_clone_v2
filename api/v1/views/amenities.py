#!/usr/bin/python3
"""
This is the module for amenities
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def all_amenities():
    """Retrieves the list of all Amenity objects"""
    objs = storage.all(Amenity)
    return jsonify([obj.to_dict() for obj in objs.values()])


@app_views.route("/amenities/<amenity_id>", methods=["GET"], strict_slashes=False)
def one_amenity(amenity_id):
    """Retrieves an Amenity object"""
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)

    return jsonify(obj.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False)
def del_amenity(amenity_id):
    """Deletes an Amenity object"""
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)

    obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Creates one Amenity"""

    new_amenity = request.get_json()
    if not new_amenity:
        abort(400, "Not a JSON")
    if "name" not in new_amenity:
        abort(400, "Missing name")

    obj = Amenity(**new_amenity)
    storage.new(obj)
    storage.save()

    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(amenity_id):
    """Updates the Amenity object"""
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)

    rq = request.get_json()
    if not rq:
        abort(400, "Not a JSON")

    for key, value in rq.items():
        if key not in ["id", "created_at", "update_at"]:
            setattr(obj, key, value)

    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)
