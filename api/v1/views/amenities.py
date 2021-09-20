#!/usr/bin/python3
"""
    New view for Amenity objects that handles
    all default RESTFul API actions
"""
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import jsonify, abort, request


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def get_amenities():
    """ Retrieves the list of all Amenity objects """
    amenities = []
    all_amenities = storage.all("Amenity")
    for amenity in all_amenities.values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['GET'])
@app_views.errorhandler(404)
def get_amenity_id(amenity_id):
    """ Retrieves a Amenity object """
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404, 'Not found')
    else:
        return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """ Deletes a Amenity object """
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404, 'Not found')
    else:
        amenity.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities',
                 strict_slashes=False,
                 methods=['POST'])
def create_amenity():
    """ Creates a Amenity """
    json_req = request.get_json()
    if json_req is None:
        abort(400, 'Not a JSON')
    elif "name" not in json_req:
        abort(400, 'Missing name')
    else:
        new_amenity = Amenity(**json_req)
        new_amenity.save()
        check_create_amenity = storage.get('Amenity', new_amenity.id)
        return jsonify(check_create_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    """ Updates a Amenity object """
    amenity_obj = storage.get('Amenity', amenity_id)
    if amenity_obj is None:
        abort(404, 'Not found')
    else:
        json_req = request.get_json()
        if json_req is None:
            abort(400, 'Not a JSON')
        else:
            amenity_obj.update(json_req)
            amenity_obj.save()
            check_update_state = storage.get('Amenity', amenity_id)
            return jsonify(check_update_state.to_dict()), 200
