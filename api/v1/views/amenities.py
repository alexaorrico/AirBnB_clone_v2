#!/usr/bin/python3
"""Amenities"""

from flask import jsonify, request, abort
from . import Amenity, app_views, storage


pl = ("name",)


@app_views.route("/amenities", methods=["GET", "POST"], strict_slashes=False)
def post_amenity():
    """Adds aamenity to the list of available agents"""
    if request.method == "GET":
        return jsonify([amenity.to_dict()
                        for amenity in storage.all(Amenity).values()])
    else:
        data = request.get_json(silent=True)
        if request.is_json and data is not None:
            load = {key: str(value) for key, value in data.items()
                    if key in pl}
            if not load.get("name", None):
                abort(400, description="Missing name")
            list = Amenity(**load)
            storage.new(list), storage.save()
            return jsonify(list.to_dict()), 201
        abort(400, description="Not a JSON")


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """Removes the amenity from the database"""
    deleted_amenity = storage.get(Amenity, str(amenity_id))
    if not deleted_amenity:
        abort(404, description="Not found")
    if request.method == "GET":
        return jsonify(deleted_amenity.to_dict())
    elif request.method == "DELETE":
        storage.delete(deleted_amenity), storage.save()
        return jsonify({})
    else:
        data = request.get_json(silent=True)
        if request.is_json and data is not None:
            [setattr(deleted_amenity, key, str(value))
             for key, value in data.items()
             if key in pl]
            deleted_amenity.save()
            return jsonify(deleted_amenity.to_dict()), 200
        abort(400, description="Not a JSON")
