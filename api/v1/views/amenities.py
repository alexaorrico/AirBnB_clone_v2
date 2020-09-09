#!/usr/bin/python3
"""
view for Amenity objects that handles all default RestFul API actions
"""

from flask import jsonify, request, abort, make_response
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


# the followings are the entendpoints of the app_view blueprint
# in other words /status == /api/v1/status and /stats == /api/v1/stats
# we create that blueprint to access to all the endpoints easily

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities_all():
    """ returns list of all Amenity objects """
    amenities_all = []
    amenities = storage.all("Amenity").values()
    for amenity in amenities:
        amenities_all.append(amenity.to_dict())
    return jsonify(amenities_all)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def amenity_get(amenity_id):
    """ handles GET method """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404, description="amenity_id not linked to any Amenity object")
    amenity = amenity.to_dict()
    return jsonify(amenity)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def amenity_delete(amenity_id):
    """ handles DELETE method """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404, description="amenity_id not linked to any Amenity object")
    storage.delete(amenity)
    storage.save()
    response = make_response(jsonify({}), 200)
    return response


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenity_post():
    """ handles POST method """
    data = request.get_json()
    if data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_amenity = Amenity(**data)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def amenity_put(amenity_id):
    """ handles PUT method """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404, description="amenity_id not linked to any Amenity object")
    data = request.get_json()
    if data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in data.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if key not in ignore_keys:
            amenity.bm_update(key, value)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)
