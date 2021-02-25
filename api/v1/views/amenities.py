#!/usr/bin/python3
"""
a new view for Amenity objects that handles
all default RestFul API actions
"""

from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False, methods=["GET", "POST"])
def amenities_base():
    """Retrieves the list of all Amenity objects"""
    if request.method == "GET":
        out = []
        for amenity in storage.all("Amenity").values():
            out.append(amenity.to_dict())
        return jsonify(out)
    if request.method == "POST":
        if not request.is_json:
            return "Not a JSON", 400
        out = Amenity(**request.get_json())
        if "name" not in out.to_dict().keys():
            return "Missing name", 400
        out.save()
        return out.to_dict(), 201


@app_views.route("/amenities/<a_id>",
                 strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def amenities_id(a_id):
    """this is a test string"""
    if request.method == "GET":
        amenity = storage.get(Amenity, a_id)
        if amenity:
            return amenity.to_dict()
        abort(404)
    if request.method == "DELETE":
        amenity = storage.get(Amenity, a_id)
        if amenity:
            amenity.delete()
            storage.save()
            return {}, 200
        abort(404)
    if request.method == "PUT":
        amenity = storage.get(Amenity, a_id)
        if amenity:
            if not request.is_json:
                return "Not a JSON", 400
            for k, v in request.get_json().items():
                setattr(amenity, k, v)
            storage.save()
            return amenity.to_dict()
        abort(404)
