#!/usr/bin/python3
""" view for Amenity """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenities(amenity_id=None):
    """ retrieves all amenities """
    if not amenity_id:
        amenities = storage.all(Amenity)
        list_amenity = []
        for amenity in amenities.values():
            list_amenity.append(amenity.to_dict())
        return jsonify(list_amenity)
    else:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            return abort(404)
        return amenity.to_dict()


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """ deletes amenity """
    if amenity_id is None:
        return abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """ post to amenities """
    if not request.json:
        return 'Not a JSON', 400
    if 'name' not in request.json:
        return 'Missing name', 400
    body = request.get_json()
    new_amenity = Amenity(**body)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """ update amenity """
    if amenity_id is None:
        return abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    if not request.json:
        return 'Not a JSON', 400
    body = request.get_json()
    for key, value in body.items():
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            continue
        setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
