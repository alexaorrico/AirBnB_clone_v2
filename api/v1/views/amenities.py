#!/usr/bin/python3
"""Flask route for amenity model"""

from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False, methods=["GET"])
@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["GET"])
def new_amenity(amenity_id=None):
    """showing all  the amenity with id"""
    am_list = []
    if amenity_id is None:
        objs = storage.all(Amenity).values()
        for new in objs:
            am_list.append(new.to_dict())
        return jsonify(am_list)
    else:
        res = storage.get(Amenity, amenity_id)
        if res is None:
            abort(404)
        return jsonify(res.to_dict())


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def new_amenity():
    """a new amenity"""
    request_json = request.get_json(force=True, silent=True)
    if not request_json:
        abort(400, "Not a JSON")
    if "name" not in request_json:
        abort(400, "Missing name")
    new_Amenity = Amenity(**request_json)
    new_Amenity.save()
    return jsonify(new_Amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["DELETE"])
def deleting_amenity(amenity_id):
    """deleting amenity"""
    new_obj = storage.get(Amenity, amenity_id)
    if new_obj is None:
        abort(404)
    storage.delete(new_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["PUT"])
def amenity_updt(amenity_id):
    """updating the amenity"""
    new_obj = storage.get(Amenity, amenity_id)
    if new_obj is None:
        abort(404)
    request_json = request.get_json(force=True, silent=True)
    if not request_json:
        abort(400, "Not a JSON")
    new_obj.name = request_json.get("name", new_obj.name)
    new_obj.save()
    return jsonify(new_obj.to_dict()), 200
