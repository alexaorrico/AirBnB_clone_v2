#!/usr/bin/python3
"""This is a module that contains views for the Cities for this API"""
from flask import jsonify
from flask import request
from flask import abort
from flask import make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """this is a function that retrieves all amenities"""
    amenities = storage.all(Amenity).values()
    amenities_list = []
    for amenity in amenities:
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_one_amenity(amenity_id):
    """this is a function that retrieves one amenity with the specified
    amenity id when the /amenities/amenity_id route is reached"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_one_amenity(amenity_id):
    """this is a function that deletes one amenity with the specified
    amenity id when the /amenities/amenity_id route is reached"""
    amenity = storage.get(Amenity, amenity_id)

    if amenity:
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """this is a function that creates one amenity when the
    /amenities route is reached"""
    if request.get_json():
        if 'name' in request.get_json():
            data = request.get_json()
            instance = Amenity(**data)
            instance.save()
            return make_response(jsonify(instance.to_dict()), 201)
        abort(400, description="Missing name")
    abort(400, description="Not a JSON")


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_one_amenity(amenity_id):
    """this is a function that updates one amenity with a specified id
    when the /amenities/amenity_id route is reached"""
    if request.get_json():
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            data = request.get_json()
            for key, value in data.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(amenity, key, value)
            storage.save()
            return make_response(jsonify(amenity.to_dict()), 200)
        abort(404)
    abort(400, description="Not a JSON")
