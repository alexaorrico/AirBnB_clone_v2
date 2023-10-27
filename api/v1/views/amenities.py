#!/usr/bin/python3
"""ammonite colony"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, Blueprint
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """asdasdadsa"""
    amenities = storage.all(Amenity).values()
    lizt = [amenity.to_dict() for amenity in amenities]
    return jsonify(lizt)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_an_amenity(amenity_id):
    """return unique amenity"""
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    ret = amenities.to_dict()
    return jsonify(ret)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_an_amenity(amenity_id):
    """asdasdasdasdasd"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_an_amenity():
    """create an amenity from an http request"""
    req = request.get_json()
    if not request.is_json:
        abort(400, description="Not a JSON")
    key = 'name'
    if key not in req:
        abort(400, description="Missing name")
    new_amenity = Amenity(**req)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_an_amenity(amenity_id):
    """ this method updates an amenity """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    req = request.get_json()
    if not request.is_json:
        abort(400, description="Not a JSON")
    for k, value in req.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, k, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
