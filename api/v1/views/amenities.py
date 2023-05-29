#!/usr/bin/python3
"""View to handle all amenites objects"""

from models import storage
from api.v1.views import app_views
from models.base_model import BaseModel
from flask import jsonify, abort, request, make_response
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """Return all amenities objects"""
    amenities = storage.all(Amenity)
    amenitiess = []
    for amen in amenities.values():
        amenitiess.append(amen.to_dict())
    return jsonify(amenitiess)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def one_amenity(amenity_id):
    """Get a single amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_amenity(amenity_id):
    """Delete an amenity obj with its id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response({}, 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Post new amenity object"""
    post_req = request.get_json()
    if not post_req:
        abort(400, "Not a JSON")
    if 'name' not in post_req:
        abort(400, "Missing name")

    new_amen = Amenity(**post_req)
    storage.new(new_amen)
    storage.save()
    return make_response(new_amen.to_dict(), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """Update the amenity object with the provided id"""
    put_req = request.get_json()
    if not put_req:
        abort(400, "Not a JSON")
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    ignore_keys = ['id', 'created_id', 'updated_at']

    for key, value in put_req.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
    storage.save()
    return make_response(amenity.to_dict(), 200)
