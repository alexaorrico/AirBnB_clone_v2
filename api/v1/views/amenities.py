#!/usr/bin/python3
"""Amenities for API"""


from flask import jsonify, request, abort
from models import storage
from api.v1.views import app
from models.amenity import Amenity


@app_view.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """All amenities"""
    all_amenities = []
    for i in storage.all("Amenity").value():
        all_amenities.append(i.to_dict())
    return jsonify(all_amenities)

@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenities(amenity_id):
    """Gets amenities"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        return jsonify(amenity.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def del_amenities(amenity_id):
    """Deletes amenities"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenities():
    """Post amenities"""
    data = request.get_json()
    if amenity is None:
        abort(400, "Not a JSON")
    if 'name' not in amenity:
        abort(400, "Missing name")
    new_amenity = amenities.Amenity(**data)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def amenity_put(amenity_id):
    """Put amenities"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key in ['id', 'created_at', 'updated_at']:
            pass
        else:
            setattr(amenity, key, value)
    storage.save()
    all_amenity = amenity.to_dict()
    return jsonify(all_amenity), 200
