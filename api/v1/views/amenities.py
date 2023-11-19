#!/usr/bin/python3
"""Create a new view for Amenity objects that
handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """list of all amenities"""
    all_amenity_list = list(map(lambda amenity: amenity.to_dict(),
                                storage.all(Amenity).values()))
    return jsonify(all_amenity_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def single_amenity(amenity_id):
    """Retrieves state object based on id"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)
    else:
        return jsonify(amenity_obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes amenity based on id"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)
    storage.delete(amenity_obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Makes an amenity"""
    obj = request.get_json()
    if not obj:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in obj:
        return make_response(jsonify({"error": "Missing name"}), 400)
    created_amenity = Amenity(**obj)
    created_amenity.save()
    return make_response(jsonify(created_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """Updates amenity"""
    amenity_obj = storage.get(Amenity, amenity_id)
    obj = request.get_json()
    if amenity_obj is None:
        abort(404)
    if not obj:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in obj.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity_obj, key, value)
    amenity_obj.save()
    return make_response(jsonify(amenity_obj.to_dict()), 200)
