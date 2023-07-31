#!/usr/bin/python3
"""
A modulde that handles all default RESTFul API actions for amenity objects
"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def all_amenities():
    """ Retrieves a list of all amenities """
    amenities_dict = storage.all("Amenity")
    return jsonify([obj.to_dict() for obj in amenities_dict.values()])


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves an amenity by its id """
    amenity_obj = storage.get("Amenity", amenity_id)
    if not amenity_obj:
        abort(404)
    return jsonify(amenity_obj.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """ Deletes an amenity """
    amenity_obj = storage.get("Amenity", amenity_id)
    if not amenity_obj:
        abort(404)
    storage.delete(amenity_obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """ Creates an Amenity """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    amenity_obj = Amenity(**data)
    amenity_obj.save()
    return make_response(jsonify(amenity_obj.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """ Updates an Amenity object"""
    amenity_obj = storage.get("Amenity", amenity_id)
    if not amenity_obj:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity_obj, key, value)
    amenity_obj.save()
    return make_response(jsonify(amenity_obj.to_dict()), 200)
