#!/usr/bin/python3
"""
view for Amenity objects that handles all default RestFul API action
"""

from flask import jsonify, request, abort, make_response
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity


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
    all_amenities = storage.all("Amenity").values()
    for amenity in all_amenities:
        if amenity.id == amenity_id:
            return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def amenity_delete(amenity_id):
    """ handles DELETE method """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    response = make_response(jsonify({}), 200)
    return response


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenity_post():
    """ handles POST method """
    dic_json = request.get_json()
    if not dic_json:
        return make_response("Not a JSON", 400)
    if "name" not in dic_json:
        return make_response("Missing name", 400)
    new_amenity = Amenity(**dic_json)
    storage.new(new_amenity)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def amenity_put(amenity_id):
    """ handles PUT method """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    dic_json = request.get_json()
    if dic_json is None:
        return make_response("Not a JSON", 400)
    for key, value in dic_json.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if key not in ignore_keys:
            setattr(amenity, key, value)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)
