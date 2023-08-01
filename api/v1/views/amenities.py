#!/usr/bin/python3
""" new Amenity object view. Handles default RESTful API actions"""
from flask import jsonify
from flask import abort
from api.v1.views import app_views
from models import storage
from flask import request
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id=None):
    """Retrieves list of all Amenity objects in storage. If id is given,
    retrieves Amenity based on given id"""
    amenities = [amenity.to_dict() for amenity in
                 storage.all("Amenity").values()]
    if amenity_id is None:
        return jsonify(amenities)
    else:
        obj = storage.get("Amenity", amenity_id)
        if obj is None:
            abort(404)
        return jsonify(obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete amenity by id"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Creates a Amenity object based on get_json request"""
    amenity = Amenity()
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data.keys():
            abort(400, 'Missing name')
    for key, value in data.items():
        setattr(amenity, key, value)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id=None):
    """Updates a Amenity object based on id using response from get_json"""
    amenity = storage.get("Amenity", amenity_id)
    data = request.get_json(silent=True)
    if amenity is None:
        abort(404)
    if data is None:
        abort(400, "Not a JSON")
    else:
        for key, value in data.items():
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
