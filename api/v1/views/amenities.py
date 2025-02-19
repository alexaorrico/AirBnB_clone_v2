#!/usr/bin/python3
""" script for State view """

from models import storage
from models.state import State
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort
from flask import request, make_response


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """Route that returns all amenities"""
    all_list = []
    amenty_dict = storage.all(Amenity)
    for _, obj in amenty_dict.items():
        all_list.append(obj.to_dict())

    return make_response(jsonify(all_list), 200)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """Route that returns a Amenity by its ID"""
    amnty_obj = storage.get(Amenity, amenity_id)
    if not amnty_obj:
        abort(404)

    return make_response(jsonify(amnty_obj.to_dict()), 200)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def amenity_delete(amenity_id):
    """ delete http request"""
    amnty_obj = storage.get(Amenity, amenity_id)
    if not amnty_obj:
        abort(404)
    storage.delete(amnty_obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenity_post():
    """post http request """
    if not request.json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")

    request_dict = request.get_json()
    obj = Amenity()

    for k, v in request_dict.items():
        setattr(obj, k, v)

    # add obj to current DB session and save it.
    storage.new(obj)
    storage.save()
    new_state = obj.to_dict()
    return make_response(jsonify(new_state), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def amenity_update(amenity_id):
    """put http request"""
    amnty_obj = storage.get(Amenity, amenity_id)
    if not amnty_obj:
        abort(404)

    if not request.json:
        abort(400, description="Not a JSON")

    new_dict = request.get_json()
    ignore_keys = {'id', 'created_at', 'updated_at'}
    for k, v in new_dict.items():
        if k not in ignore_keys:
            setattr(amnty_obj, k, v)

    storage.save()
    return make_response(jsonify(amnty_obj.to_dict()), 200)
