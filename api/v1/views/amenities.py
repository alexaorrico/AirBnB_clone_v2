#!/usr/bin/python3
"""
    this module contains flask app routes
        flask APP routes:
        methods:
            GET:
                /amenities:
                    list all Amenitys
                /amenities/<amenity_id>:
                    display Amenity dictionary using ID
            DELETE:
                /amenities/<amenity_id>:
                    delete a Amenity using ID
            POST:
                /amenities:
                    creates a new Amenity
            PUT:
                /amenities/<amenity_id>:
                    update Amenity object using ID
"""

from api.v1.views import app_views
from flask import abort, jsonify, request

# import Amenity and Storage models
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"])
def get_Amenitys():
    """display all amenities"""
    amenity_list = []
    [amenity_list.append(amenity.to_dict())
     for amenity in storage.all(Amenity).values()]
    return jsonify(amenity_list)


@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def get_Amenity(amenity_id):
    """diplay a Amenity using ID"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    return obj.to_dict()


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def remove_Amenity(amenity_id):
    """delete a Amenity instance using ID"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"])
def create_Amenity():
    """creates a new Amenity instance"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    obj = Amenity(**(request.get_json()))
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_Amenity(amenity_id):
    """update a Amenity instance using ID"""
    ignore_keys = ["id", "created_at", "updated_at"]
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    [setattr(obj, key, value) for key, value in request.get_json().items()
     if key not in ignore_keys]
    obj.save()
    return jsonify(obj.to_dict()), 200
