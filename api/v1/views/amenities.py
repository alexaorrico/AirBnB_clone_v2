#!/usr/bin/python3
""" index routes """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities")
def get_amenities():
    """get all amenities"""
    amenities = []
    for amenity in storage.all(Amenity).values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route("/amenities/<amenity_id>")
def get_amenity(amenity_id):
    """get amenity"""
    res = storage.get(Amenity, amenity_id)
    if res is None:
        abort(404)
    return jsonify(res.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """delete amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"])
def create_amenity():
    """add new amenity"""
    if request.json is None:
        abort(400, "Not a JSON")
    data = request.get_json()
    if data.get('name') is None:
        return "Missing name", 400
    new_amenity = Amenity(name=request.json['name'])
    # new_city = City(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    """update amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    data = request.get_json()
    if request.json is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
