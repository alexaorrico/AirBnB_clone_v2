#!/usr/bin/python3
"""
Module that creates a view for Amenity
"""

from flask import jsonify, abort, request
from api.v1.views.__init__ import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def amenity_index(amenity_id=None):
    """
    Retrieves a list of all amenity objects on
    GET /api/v1/amenities request
    """
    if amenity_id is None:
        amenities_obj = list(storage.all(Amenity).values())
        amenities_list = list(amenity.to_dict() for amenity in amenities_obj)
        return jsonify(amenities_list)
    else:
        obj = storage.get(Amenity, amenity_id)
        if obj is not None:
            return jsonify(obj.to_dict())
        else:
            abort(404)


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def post_amenity():
    """
    Posts an Amenity object on
    POST /api/v1/amenities request
    """
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        abort(400, description='Not a JSON')
    else:
        json = request.get_json()
        if json is None:
            abort(400, description='Not a JSON')
        if 'name' in json.keys():
            obj = Amenity(**json)
            obj_id = obj.id
            obj.save()
            return amenity_index(obj_id), 201
        else:
            abort(400, description='Missing name')


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """
    Deletes a amenity object on
    DELETE /api/v1/amenities/<amenity_id> request
    """
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """
    Replaces a amenity object on
    PUT /api/v1/amenities/<amenity_id> request
    """
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)

    else:
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            abort(400, description='Not a JSON')
        else:
            json = request.get_json()
            if json is None:
                abort(400, description='Not a JSON')
            for key, value in json.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(obj, key, value)
                storage.save()
            return amenity_index(amenity_id), 200
