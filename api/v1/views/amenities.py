#!/usr/bin/python3
'''Module containing instructions for the flask blueprint app_views'''
from api.v1.views import app_views
from api import mapped_classes
from flask import jsonify, abort, request, make_response
from models import storage


@app_views.route('/amenities',
                 strict_slashes=False, methods=['GET'])
def all_amenities():
    '''Retrieves all Amenity objects'''
    content = storage.all("Amenity")
    rqd_info = []
    for key, value in content.items():
        rqd_info.append(value.to_dict())
    return jsonify(rqd_info)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def post_make_new_amenity():
    '''Create an Amenity Object else raise error'''
    content = request.get_json()
    if not content:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in content:
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_amenity = mapped_classes["Amenity"](**content)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['GET'])
def get_specific_amenity(amenity_id):
    '''Get a specific amenity by the id given'''
    content = storage.get("Amenity", amenity_id)
    if content is None:
        abort(404)
    else:
        return jsonify(content.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_spcific_amenity(amenity_id):
    '''Delete a specific Amenity else raise an error'''
    content = storage.get("Amenity", amenity_id)
    if content is None:
        abort(404)
    else:
        storage.delete(content)
        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['PUT'])
def update_specified_amenity(amenity_id):
    '''Update a sepcific Amenity as identified by ID'''
    content = storage.get("Amenity", amenity_id)
    if content is None:
        abort(404)
    else:
        update_dict = request.get_json()
        if not update_dict:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        update_dict.pop("id", None)
        update_dict.pop("created_at", None)
        update_dict.pop("updated_at", None)
        for key, value in update_dict.items():
            setattr(content, key, value)
        content.save()
        return jsonify(content.to_dict()), 200
