#!/usr/bin/python3
"""RestFul API actions for Amenities"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@swag_from('documentation/amenity/all_amenities.yml')
def get_amenities():
    """Retrieves the list of all Amenity"""
    a_list = [obj.to_dict() for obj in storage.all(Amenity).values()]
    return jsonify(a_list)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/amenity/get_id.yml', methods=['GET'])
def get_amenity(amenity_id):
    """Retrieves a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/amenity/delete.yml', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities/', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/amenity/post.yml', methods=['POST'])
def create_amenity():
    """Creates a Amenity"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json()
        return make_response(jsonify({"error": "Missing name"}), 400)
    obj = Amenity(**(request.get_json()))
    obj.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/amenity/put.yml', methods=['PUT'])
def post_amenity(amenity_id):
    """Updates a Amenity object"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
