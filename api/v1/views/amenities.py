#!/usr/bin/python3
""" flask module to manage the stored amenities """
from models.amenity import Amenity
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage


@app_views.route(
    '/amenities',
    strict_slashes=False,
    methods=['GET', 'POST']
)
@app_views.route(
    '/amenities/<amenity_id>',
    strict_slashes=False, methods=['GET', 'PUT', 'DELETE']
)
def amenities(amenity_id=None):
    """ handles all default RestFul API actions inside amenities"""
    if request.method == 'GET' and amenity_id is None:
        return all_amenities()
    elif request.method == 'GET' and amenity_id:
        return get_amenity(amenity_id)
    elif request.method == 'DELETE':
        return delete_amenity(amenity_id)
    elif request.method == 'POST':
        return create_amenity()
    elif request.method == 'PUT':
        return update_amenity(amenity_id)


def update_amenity(amenity_id):
    """ it update an amenity """
    ignored_keys = ['id', 'created_at', 'updated_at']
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity_json = request.get_json()
    if amenity_json is None:
        abort(400, 'Not a JSON')

    for key in amenity_json.keys():
        if key in ignored_keys:
            continue
        if getattr(amenity, key):
            setattr(amenity, key, amenity_json[key])
        storage.save()
        return jsonify(amenity.to_dict()), 200


def create_amenity():
    """ it create an amenity from a http request
    the new amenity information is expected to be
    json string
    """
    amenity_json = request.get_json()
    if amenity_json is None:
        abort(400, 'Not a JSON')
    if amenity_json.get('name') is None:
        abort(400, "Missing name")
    amenity = Amenity(**amenity_json)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


def delete_amenity(amenity_id):
    """ it delete the amenity corresponding to the amenity_id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


def get_amenity(amenity_id):
    """ it get the amenity corresponding to the amenity_id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


def all_amenities():
    """ it retrieve all the amenities """
    amenities_list = []
    for amenity in storage.all(Amenity).values():
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)
