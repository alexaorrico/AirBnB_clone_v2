#!/usr/bin/python3
""" Flask routes utilizing the  `app_views` Blueprint for
URI subpaths associated to `Amenity` objects.
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'],
                 strict_slashes=False)
def GET_all_Amenity():
    """ Provides JSON list of storage-based `Amenity` instance.

    Return:
        All instances of `Amenity` in a JSON list
    """
    amenity_list = []
    for amenity in storage.all(Amenity).values():
        amenity_list.append(amenity.to_dict())

    return jsonify(amenity_list)


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def GET_Amenity(amenity_id):
    """ Returns the storage instance of `Amenity` via URI subpath id.

    Args:
        amenity_id: The storage-based uuid of the `Amenity` instance

    Return:
        A 404 error message or an instance of `Amenity` with
    the matching uuid
    """
    amenity = storage.get(Amenity, amenity_id)

    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def DELETE_Amenity(amenity_id):
    """ URI subpath id Deletes `Amenity` object in storage

    Args:
        amenity_id: uuid of the stored instance of `Amenity`

    Return:
        Dictionary empty and response status 200
    or 404 in the event of an error.
    """
    amenity = storage.get(Amenity, amenity_id)

    if amenity:
        storage.delete(amenity)
        storage.save()
        return ({})
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def POST_Amenity():
    """ Generates a fresh instance of `Amenity` in storage

    Return:
        Dictionary empty and response status 200, or
    404 in the event of an error
    """
    req_dict = request.get_json()
    if not req_dict:
        return (jsonify({'error': 'Not a JSON'}), 400)
    elif 'name' not in req_dict:
        return (jsonify({'error': 'Missing name'}), 400)
    new_Amenity = Amenity(**req_dict)
    new_Amenity.save()

    return (jsonify(new_Amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def PUT_Amenity(amenity_id):
    """ Modifies `Amenity` object in storage using the id in the 
    URI subpath and arguments from HTTP body request JSON dict.

    Args:
        amenity_id: Storage based uuid of the `Amenity` instance

    Return:
        Dictionary empty and response status 200
    or 404 in the event of an error
    """
    amenity = storage.get(Amenity, amenity_id)
    req_dict = request.get_json()

    if amenity:
        if not req_dict:
            return (jsonify({'error': 'Not a JSON'}), 400)
        for key, value in req_dict.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        storage.save()
        return (jsonify(amenity.to_dict()))
    else:
        abort(404)
