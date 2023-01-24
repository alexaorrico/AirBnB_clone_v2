#!/usr/bin/python3
from models import storage
from models.amenity import Amenity
from . import app_views
from flask import jsonify, abort, request

@app_views.route("/amenities")
def amenities():
    amenities = storage.all(Amenity)
    amen_list = []
    for amenity in amenities.values():
        amen_list.append(amenity.to_dict())
    return jsonify(amen_list)

@app_views.route("/amenities/<amenity_id>")
def amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())

@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})

@app_views.route("/amenities", methods=["POST"])
def create_amenity():
    if request.content_type != "application/json":
        abort(404)
    data = request.get_json()
    if "id" in data:
        data.pop("id")
    if "created_at" in data:
        data.pop("created_at")
    if "updated_at" in data:
        data.pop("updated_at")
    for key, value in data.items():
        amenity.__setattr__(key, value)
    amenity.save()
    return jsonify(amenity.to_dict())


