#!/usr/bin/python3
"""Amenity objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all("Amenity").values()
    amenities_list = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """Retrieves, Deletes or Updates a Amenity object by it's id"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    if request.method == "GET":
        return jsonify(amenity.to_dict())

    elif request.method == "DELETE":
        amenity.delete()
        storage.save()
        return jsonify({}), 200

    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    if "name" not in data:
        return "Missing name", 400
    nope = {"id", "created_at", "updated_at"}
    [setattr(amenity, key, val) for key, val in data.items() if key not in nope]
    amenity.save()
    return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a Amenity object"""
    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    if "name" not in data:
        return "Missing name", 400
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201