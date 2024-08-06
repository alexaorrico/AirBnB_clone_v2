#!/usr/bin/python3
""" """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.amenity import Amenity
from models import storage
AMN = '/amenities/<amenity_id>'


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ """
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route(AMN, methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """ """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ """
    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")

    if "name" not in data:
        abort(400, description="Missing name")

    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route(AMN, methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """ """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if not request.is_json:
        abort(400, "Not a json")

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)

    amenity.save()
    return jsonify(amenity.to_dict()), 200


@app_views.route(AMN, methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """ """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200
