#!/usr/bin/python3
"""Flask route for amenity model"""

from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET', 'POST'])
def amenities():
    """route to return all amenities"""
    if request.method == "GET":
        amenities_dict = storage.all(Amenity)
        amenities_list = [obj.to_dict() for obj in amenities_dict.values()]
        return jsonify(amenities_list)

    if request.method == "POST":
        request_json = request.get_json()
        if request_json is None:
            abort(400, "Not a JSON")
        if request_json.get("name") is None:
            abort(400, "Missing name")

        newAmenity = Amenity(**request_json)
        newAmenity.save()
        return jsonify(newAmenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["GET", "DELETE", "PUT"])
def amenity(amenity_id=None):
    """Get, update or delete state with amenity id"""
    amenity_obj = storage.get(Amenity, amenity_id)

    if amenity_obj is None:
        abort(404, "Not found")

    if request.method == "GET":
        return jsonify(amenity_obj.to_dict())

    if request.method == "DELETE":
        amenity_obj.delete()
        storage.save()
        return jsonify({})

    if request.method == "PUT":
        request_json = request.get_json()
        if request_json is None:
            abort(400, "Not a JSON")
        amenity_obj.update(request_json)
        return jsonify(amenity_obj.to_dict()), 200
