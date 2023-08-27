#!/usr/bin/python3
""" View for Amenities """

from flask import jsonify, abort, request, make_response
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage


@app_views.route('/amenities',
                 methods=['GET'],
                 strict_slashes=False)
def get_amenities():
    """ Retrieve the list of all Amenity objects """
    amenities_dict = storage.all(Amenity)
    amenities_list = []
    for amenity in amenities_dict.values():
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieve a specific Amenity object by its ID """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes an Amenity object. """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/amenities',
                 methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """ Creates an Amenity object. """
    request_dict = request.get_json(silent=True)
    if request_dict is not None:
        if 'name' in request_dict.keys() and request_dict['name'] is not None:
            new_amenity = Amenity(**request_dict)
            new_amenity.save()
            return make_response(jsonify(new_amenity.to_dict()), 201)
        return make_response(jsonify({'error': 'Missing name'}), 400)
    return make_response(jsonify({"error": "Not a JSON"}), 400)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates an Amenity object. """
    request_dict = request.get_json(silent=True)
    if request_dict is not None:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        for key, val in request_dict.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, val)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 200)
    return make_response(jsonify({"error": "Not a JSON"}), 400)
