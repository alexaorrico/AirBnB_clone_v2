#!/usr/bin/python3
""" Blueprint for API """
from flask import Blueprint, jsonify, make_response, request, abort
from models import storage
from models.amenity import Amenity

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ get amenities """
    amenities = storage.all(Amenity).values()
    amenities = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """ get amenity """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """ delete amenity """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """ post amenity """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    amenity = Amenity(**request.get_json())
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """ put amenity """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)
