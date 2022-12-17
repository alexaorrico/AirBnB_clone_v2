#!/usr/bin/python3
""" Amenity objects that handles all default RESTFul API """

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State
from models.amenity import Amenity

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities_all():
    """Retrieves the list of all Amenity objects"""
    amenities = []
    for i in storage.all(Amenity).values():
        amenities.append(i.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id=None):
    """Retrieves a Amenity object: GET /api/v1/amenities/<amenity_id>"""
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    return jsonify(amenities.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id=None):
    """Deletes a Amenity object:: DELETE"""
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    storage.delete(amenities)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_state():
    """Creates a Amenity: POST /api/v1/amenities"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    new_amenities = Amenity(**request.get_json())
    new_amenities.save()
    return make_response(jsonify(new_amenities.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """Updates a Amenity object: PUT"""
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404, description="Not found")
    if not request.get_json():
        abort(400, description="Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['state_id', 'create_at', 'update_at']:
            setattr(amenities, key, value)
    storage.save()
    return make_response(jsonify(amenities.to_dict()), 200)
