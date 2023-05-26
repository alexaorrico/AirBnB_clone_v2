#!/usr/bin/python3
"""New view for Amenity objects that handles all"""

from models.amenity import Amenity
from flask import Flask, abort, jsonify, make_response
from flask import request
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage


@app_views.route('/amenities', methods=['GET'])
def all_amenities():
    """Return all Amenities"""
    amenities = storage.all(Amenity).values()
    list_ame = []
    for amenity in amenities:
        list_ame.append(amenity.to_dict())
    return jsonify(list_ame)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def amenity_id(amenity_id=None):
    """Return amenity"""
    if amenity_id is not None:
        my_amenity_obj = storage.get(Amenity, amenity_id)
        if my_amenity_obj is None:
            abort(404)
        else:
            return jsonify(my_amenity_obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def amenity_delete(amenity_id=None):
    """DELETE amenity"""
    if amenity_id is not None:
        my_amenity_obj = storage.get(Amenity, amenity_id)
        if my_amenity_obj is None:
            abort(404)
        else:
            storage.delete(my_amenity_obj)
            return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'])
def amenity_post():
    """POST amenity"""
    my_json = request.get_json(silent=True)
    if my_json is not None:
        if "name" in my_json:
            name = my_json["name"]
            new_city = Amenity(name=name)
            new_city.save()
            return make_response(jsonify(new_city.to_dict()), 201)
        else:
            abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")


@app_views.route('amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id=None):
    """PUT amenity"""
    if amenity_id is not None:
        my_amenity_obj = storage.get(Amenity, amenity_id)
        if my_amenity_obj is None:
            abort(404)
        else:
            update_ = request.get_json(silent=True)
            if update_ is not None:
                for key, value in update_.items():
                    setattr(my_amenity_obj, key, value)
                    my_amenity_obj.save()
                return make_response(jsonify(my_amenity_obj.to_dict()), 200)
            else:
                abort(400, "Not a JSON")
