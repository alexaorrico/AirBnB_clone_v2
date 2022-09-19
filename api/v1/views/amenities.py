#!/usr/bin/python3
"""amenites view"""
from models.amenity import Amenity
from models import storage
from flask import Flask, abort, jsonify, request, make_response
from api.v1.views import app_views


@app_views.route('/amenities',
                 methods=['GET'], strict_slashes=False)
def get_amenity():
    """return a list of dictionary amenity"""
    states = storage.all(Amenity).values()
    Amenities_list = []
    for Amenity in Amenities_list:
        Amenities_list.append(Amenity.to_dict())
    return jsonify(Amenities_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """return amenity for a given id"""
    my_amenity = storage.get(Amenity, amenity_id)
    if my_amenity is None:
        abort(400)
    return jsonify(my_amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """delete amenity for a given id and return an empty dictionary"""
    my_amenity = storage.get(Amenity, amenity_id)
    storage.delete(my_amenity)
    storage.save()
    if my_amenity is None:
        abort(400)
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """post a new amenity as a dictionary"""
    try:
        form = request.get_json()
    except Exception as e:
        abort(400, "Not a JSON")

    if form['name'] is None:
        abort(400, "Missing name")
    my_amenity = Amenity(**form)
    storage.new(my_amenity)
    storage.save()
    return jsonify(my_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity_by_id(amenity_id):
    """delete amenity for a given id and return an empty dictionary"""
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, 'Not a JSON')
    my_amenity = storage.get(Amenity, amenity_id)
    if my_amenity:
        for key, value in data.items():
            if key not in ("id", "created_at", "updated_at"):
                setattr(my_amenity, key, value)
        storage.save()
    else:
        abort(404)
    return jsonify(my_amenity.to_dict()), 200
