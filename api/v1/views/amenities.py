#!/usr/bin/python3
"""
File that configures the routes of amenity
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route("/amenities", strict_slashes=False)
@app_views.route("/amenities/<amenity_id>", strict_slashes=False)
def get_amenity(amenity_id=None):
    """
    Route to get amenities
    """
    list_obj = []
    if not amenity_id:
        for val in storage.all("Amenity").values():
            list_obj.append(val.to_dict())
        return jsonify(list_obj)
    amenity_obj = storage.get("Amenity", amenity_id)
    if amenity_obj:
        return jsonify(amenity_obj.to_dict())
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id=None):
    """
    deletes a Amenity object
    """
    amenity_obj = storage.get("Amenity", amenity_id)
    if amenity_obj:
        storage.delete(amenity_obj)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/amenities", methods=["POST"],
                 strict_slashes=False)
def post_amenity():
    """
    Route that create a new Amenity
    """
    try:
        data = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    if data:
        if "name" in data:
            obj = Amenity(**data)
            obj.save()
            return (jsonify(obj.to_dict()), 201)
        else:
            abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")


@app_views.route("/amenities", methods=["PUT"], strict_slashes=False)
@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def put_amenity(amenity_id=None):
    """
    Route that update an Amenity
    """
    obj = storage.get("Amenity", amenity_id)
    if amenity_id and obj:
        try:
            data = request.get_json()
        except Exception:
            abort(400, "Not a JSON")
        if data:
            for key, value in data.items():
                if (key != "id" and key != "amenity_id" and
                        key != "created_at" and key != "updated_at"):
                    setattr(obj, key, value)

            obj.save()
            return (jsonify(obj.to_dict()))
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
