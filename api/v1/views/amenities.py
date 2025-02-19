#!/usr/bin/python3
""" Create a view for the Amenity Objects """


from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route("/amenities", methods=["GET"])
def all_amenities():
    """ Retrieve all Amenity objects """
    amenities = storage.all(Amenity)
    amenity_list = [amenity.to_dict() for amenity in amenities.values()]
    return jsonify(amenity_list)


@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def one_amenity(amenity_id):
    """ Retrieves a Amenity Object """
    amenities = storage.get(Amenity, amenity_id)
    if not amenities:
        abort(404)
    return jsonify(amenities.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """ Retrieves a Amenity Object """
    one_amenity = storage.get(Amenity, amenity_id)
    if not one_amenity:
        abort(404)
    storage.delete(one_amenity)
    storage.save()
    return {}, 200


@app_views.route("/amenities", methods=["POST"])
def create_amenity():
    """ Create a new Amenity object """
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    new_amenity = Amenity(name=data["name"])

    storage.new(new_amenity)
    storage.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    """ Update a Amenity object """
    one_amenity = storage.get(Amenity, amenity_id)

    if not one_amenity:
        return jsonify({"error": "Not found"}), 404

    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(one_amenity, key, value)

    storage.save()
    return jsonify(one_amenity.to_dict()), 200
