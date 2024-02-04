#!/usr/bin/python3
""" This module contains a blue print for a restful API that
    works for city objects
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


# @app_views.route('/amenities/', methods=['GET', 'POST'])
@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def post_get_amenity_obj():
    """ This function contains two http method handler

        GET:
            return the all amenity objects
        POST:
            create a new amenity object
    """
    if request.method == 'GET':
        amenity_objects = storage.all(Amenity)
        amenity_list = []
        for amenity in amenity_objects.values():
            amenity_list.append(amenity.to_dict())
        return jsonify(amenity_list)
    elif request.method == 'POST':
        amenity_dict = request.get_json()
        if not amenity_dict 
            abort(400, description="Not a JSON")
        if "name" not in amenity_dict:
            abort(400, description="Missing name")
        new_amenity = Amenity(**amenity_dict)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route(
        '/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
        strict_slashes=False
        )
def delete_put_get_amenity_obj(amenity_id):
    """ This function contains two http method handler

        GET:
            get the amenity object with the respective id
        DELETE:
            delete the amenity object with the respective id
        PUT:
            update the amenity object with the respective id
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    elif request.method == 'GET':
        return jsonify(amenity.to_dict())
    elif request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        amenity_dict = request.get_json()
        if not amenity_dict:
            abort(400, description="Not a JSON")
        for key, value in amenity_dict.items():
            if key != "id" and key != "created_at" and key != "updated_at":
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
