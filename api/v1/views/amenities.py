#!/usr/bin/python3
"""function to create the route status"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities')
def amenities():
    """retrieve all objs"""
    amenities = []
    for val in storage.all("Amenity").values():
        amenities.append(val.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>')
def amenities_id(amenity_id):
    """get amenity with his id"""
    for val in storage.all("Amenity").values():
        if val.id == amenity_id:
            return jsonify(val.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def amenities_delete(amenity_id):
    """delete a obj with his id"""
    amenities = storage.get("Amenity", amenity_id)
    if amenities is None:
        abort(404)
    storage.delete(amenities)
    storage.save()
    storage.close()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'])
def amenities_create():
    """create amenity"""
    if request.is_json:
        data = request.get_json()
    else:
        msg = "Not a JSON"
        return jsonify({"error": msg}), 400

    if "name" not in data:
        msg = "Missing name"
        return jsonify({"error": msg}), 400

    var = Amenity(**data)
    storage.new(var)
    storage.save()
    return jsonify(var.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def amenities_update(amenity_id):
    """update amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if request.is_json:
        data = request.get_json()
    else:
        msg = "Not a JSON"
        return jsonify({"error": msg}), 400

    for k, v in data.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(amenity, k, v)

    storage.save()
    return jsonify(amenity.to_dict()), 200
