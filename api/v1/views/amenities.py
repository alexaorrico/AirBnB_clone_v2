#!/usr/bin/python3
"""Defines all the places routes"""
from flask import jsonify, request, abort
from api.v1.views import amenities_view
from models import storage
from models.amenity import Amenity


@amenities_view.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    """ Retrieves the list of amenities objects """
    r_amenities = storage.all(Amenity)
    return jsonify([obj.to_dict() for obj in r_amenities.values()])


@amenities_view.route('amenities/<amenity_id>', methods=['GET'],
                      strict_slashes=False)
def get_amenity_id(amenity_id):
    """ Retrieves amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@amenities_view.route('/amenities/<amenity_id>', methods=['DELETE'],
                      strict_slashes=False)
def del_amenity(amenity_id):
    """ Deletes an Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@amenities_view.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """ Creates a Amenity object """
    new_amenity = request.get_json()
    if not new_amenity:
        abort(400, "Not a JSON")
    if "name" not in new_amenity:
        abort(400, "Missing name")
    name = new_amenity['name']
    amenity = Amenity(name=name)
    amenity.save()

    return jsonify(amenity.to_dict()), 201


@amenities_view.route('/amenities/<amenity_id>', methods=['PUT'],
                      strict_slashes=False)
def put_amenity(amenity_id):
    """ Updates a Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    data_request = request.get_json()
    if not body_data:
        abort(400, "Not a JSON")

    for key, value in data_request.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(amenity, key, value)

    storage.save()
    return jsonify(amenity.to_dict()), 200
