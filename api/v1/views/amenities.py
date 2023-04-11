#!/usr/bin/python3
""" handles all default RESTFul API actions for Amenity """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def list_amenities():
    """ retrieves list of all Amenity objects """
    amenities = storage.all(Amenity)
    amenities_list = []
    for amenity in amenities.values():
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def amenity_by_id(amenity_id):
    """ retrieves an Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        amenity_id = amenity.to_dict()
    return jsonify(amenity_id)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """ deletes an Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()
    return (jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ creates an Amenity """
    data_json = request.get_json()
    if not data_json:
        abort(400, description="Not a JSON")
    if 'name' not in data_json:
        abort(400, description="Missing name")
    new_amenity = Amenity(**data_json)
    new_amenity.save()
    return (jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """ updates an Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    data_json = request.get_json()
    if not amenity:
        abort(404)
    elif not data_json:
        abort(400, description="Not a JSON")
    else:
        for key, value in data_json.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        storage.save()
        return (jsonify(amenity.to_dict()), 200)
