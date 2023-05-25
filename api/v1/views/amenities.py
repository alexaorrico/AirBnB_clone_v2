#!/usr/bin/python3
""" Configures RESTful api for the amenities route """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET", "POST"], strict_slashes=False)
def amenities():
    """ configures the amenities route """

    if request.method == "GET":
        amenities = storage.all(Amenity)
        amenities_dict = [amenity.to_dict() for amenity in amenities.values()]

        return jsonify(amenities_dict)
    else:
        try:
            json_dict = request.get_json()
        except Exception:
            abort(400, "Not a JSON")

        try:
            name = json_dict["name"]
        except KeyError:
            abort(400, "Missing name")

        new_amenity = Amenity()
        new_amenity.name = name

        storage.new(new_amenity)
        storage.save()

        return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def amenities_id(amenity_id):
    """ configures the amenities/<amenity_id> route """

    amenity = storage.get("Amenity", amenity_id)

    if not amenity:
        abort(404)

    if request.method == "GET":
        return jsonify(amenity.to_dict())
    elif request.method == "DELETE":
        storage.delete(amenity)
        storage.save()

        return jsonify({}), 200
    else:
        try:
            json_dict = request.get_json()
        except Exception:
            abort(400, "Not a JSON")

        keys_to_ignore = ["id", "created_at", "updated_at"]
        for key, val in json_dict.items():
            if key not in keys_to_ignore:
                setattr(amenity, key, val)

        storage.new(amenity)
        storage.save()

        return jsonify(amenity.to_dict()), 200
