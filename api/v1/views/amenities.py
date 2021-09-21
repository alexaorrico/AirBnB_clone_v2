#!/usr/bin/python3
""" Handle RESTful API request for states"""

from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage


@app_views.route('/amenities',
                 methods=['GET'],
                 strict_slashes=False)
def all_amenities():
    """ GET ALL AMENITIES """
    objs = storage.all(Amenity).values()
    list_obj = []
    for obj in objs:
        list_obj.append(obj.to_dict())

    return jsonify(list_obj)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_amenities(amenity_id):
    """ Retrieves a specific State """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    obj = storage.get(Amenity, amenity_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/amenities',
                 methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """Creates a amenity """

    if not request.get_json():
        abort(400, description="Not a JSON")
    else:
        data = request.get_json()

    if 'name' in data:
        new_amenity = Amenity(**data)
        new_amenity.save()
    else:
        abort(400, description="Missing name")

    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """update a State: POST /api/v1/states"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    obj = storage.get(Amenity, amenity_id)

    if not obj:
        abort(404)

    data = request.get_json()

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(obj, key, value)
    obj.save()

    return make_response(jsonify(obj.to_dict()), 200)
