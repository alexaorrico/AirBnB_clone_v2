#!/usr/bin/python3
""" Methos API for object Amenities """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', defaults={'amenity_id': None},
                 methods=['GET'],
                 strict_slashes=False)
@app_views.route('/amenities/<path:amenity_id>')
def get_amenity(amenity_id):
    """ Get all or one Amenity object """
    if amenity_id is None:
        all_amenities = storage.all(Amenity)
        return jsonify([
            amenity.to_dict() for amenity in all_amenities.values()
            ])

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Delete a Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """ Create a new Amenity object """
    request_amenity = request.get_json()
    if not request_amenity:
        abort(400, "Not a JSON")
    if "name" not in request_amenity:
        abort(400, "Missing name")
    amenity = Amenity(**request_amenity)
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """ Update a Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    request_amenity = request.get_json()
    if not request_amenity:
        abort(400, "Not a JSON")

    for key, value in request_amenity.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
