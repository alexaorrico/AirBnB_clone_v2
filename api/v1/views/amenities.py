#!/usr/bin/python3
""" Module for amenity object view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities():
    """ Returns all amenity objects """
    amenities_dict_list = [amenity.to_dict() for amenity in
                           storage.all("Amenity").values()]
    return jsonify(amenities_dict_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_id(amenity_id):
    """ Method retrieves amenity object with certain id """
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Method deletes amenity object based off of its id """
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def post_amenity():
    """ Method creates new amenity object """
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    if body.get("name") is None:
        abort(400, "Missing name")
    amenity = Amenity(**body)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """ Method updates an amenity object based off its id """
    amenity = storage.get("Amenity", amenity_id)
    body = request.get_json()
    if not amenity:
        abort(404)
    if not body:
        abort(400, "Not a JSON")
    for k, v in body.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict())
