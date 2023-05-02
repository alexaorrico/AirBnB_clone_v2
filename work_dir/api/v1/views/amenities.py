#!/usr/bin/python3
"""
A view for Amenity object that handles all restful api
"""
from flask import jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET'], strict_slashes=False)
def all_amenity_objs():
    """
    retrieve the list of all amenity objects
    """
    a_list = []
    amenities = storage.all(Amenity)
    for amenity in amenities.values():
        a_list.append(amenity.to_dict())
    return jsonify(a_list)


@app_views('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_an_amenity(amenity_id):
    """return a single instance of amenity when called
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity = amenity.to_dict()
    return jsonify(amenity)


@app_views.route("/amenities/amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_obj(amenity_id):
    """
    delete an amenity instance from the list
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_newAmenity_obj():
    """
    creates a new instance of the amenity object
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    amenityToPost = request.get_json()
    newAmenity = Amenity(**amenityToPost)
    storage.new()
    storage.save(newAmenity)
    return jsonify(newAmenity), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """updates the amenity instance"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    update = request.get_json()
    for key, value in update.items():
        if key not in ['id', 'created_at', 'updated_at']:
            updated_amenity = setattr(amenity, key, value)

    storage.save()
    return jsonify(updated_amenity.to_dict()), 200
