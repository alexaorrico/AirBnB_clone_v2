#!/usr/bin/python3
""" view for Amenity objects that handles all default RestFul API actions """
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Retrieves the list of all Amenity objects """
    amenities = storage.all(Amenity)
    return jsonify([amenity.to_dict() for amenity in amenities.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_id(amenity_id):
    """ Retrieves Amenity object """
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity_id(amenity_id):
    """ Deletes a Amenity object """
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenities():
    """ Creates a Amenity object """
    new_amenity = request.get_json()
    if not new_amenity:
        abort(400, "Not a JSON")
    if "name" not in new_amenity:
        abort(400, "Missing name")
    amenity = Amenity(**new_amenity)
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity_id(amenity_id):
    """ Updates a Amenity object """
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    my_dict = request.get_json()
    if not my_dict:
        abort(400, "Not a JSON")
    for key, value in my_dict.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
