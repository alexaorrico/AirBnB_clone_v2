#!/usr/bin/python3
"""state view"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def all_amenities():
    """retrieve all amenities"""
    amenities_list = []
    for amenity in storage.all(Amenity).values():
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def an_amenity(amenity_id):
    """retrieve an amenity with its id"""
    try:
        amenity = storage.get(Amenity, amenity_id)
        return jsonify(amenity.to_dict())
    except Exception:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete an Amenity object"""
    if amenity_id is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def POST_request_amenity():
    """"post request"""
    data = request.get_json()
    if not data:
        return abort(400, {'message': 'Not a JSON'})
    if 'name' not in data:
        abort(400)
        return abort(400, {'message': 'Missing name'})
    # creation of a new state
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def PUT_amenity(amenity_id):
    """Put request"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json()
    if not data:
        return abort(400, {'message': 'Not a JSON'})
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
