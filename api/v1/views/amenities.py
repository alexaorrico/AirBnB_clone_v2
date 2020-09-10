#!/usr/bin/python3
"""View for Amenity objects that handles all default RestFul API"""
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Returns a json object with all the amenities"""
    list_dict = []
    for obj in storage.all(Amenity).values():
        list_dict.append(obj.to_dict())
    return jsonify(list_dict), 200


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Returns a json object with the amenity with given id"""
    obj = storage.get(Amenity, amenity_id)
    if (obj):
        return jsonify(obj.to_dict()), 200
    else:
        abort(404)


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete a amenity"""
    obj = storage.get(Amenity, amenity_id)
    if (obj):
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create a new amenity"""
    conten = request.get_json()
    if conten is None:
        return "Not a JSON", 400
    if conten.get('name') is None:
        return "Missing name", 400
    else:
        new_obj = Amenity(**conten)
        storage.new(new_obj)
        storage.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Update a amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, attr, val)
    storage.save()
    return jsonify(amenity.to_dict())
