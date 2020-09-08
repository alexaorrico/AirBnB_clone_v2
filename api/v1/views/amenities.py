#!/usr/bin/python3
""" Flask routes for `Amenity` object related URI subpaths using the
`app_views` Blueprint.
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'],
                 strict_slashes=False)
def GET_all_Amenity():
    """ Returns JSON list of all `Amenity` instances in storage

    Return:
        JSON list of all `Amenity` instances
    """
    amenity_list = []
    for amenity in storage.all(Amenity).values():
        amenity_list.append(amenity.to_dict())

    return jsonify(amenity_list)


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def GET_Amenity(amenity_id):
    """ Returns `Amenity` instance in storage by id in URI subpath

    Args:
        amenity_id: uuid of `Amenity` instance in storage

    Return:
        `Amenity` instance with corresponding uuid, or 404 response
    on error
    """
    amenity = storage.get(Amenity, amenity_id)

    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def DELETE_Amenity(amenity_id):
    """ Deletes `Amenity` instance in storage by id in URI subpath

    Args:
        amenity_id: uuid of `Amenity` instance in storage

    Return:
        Empty dictionary and response status 200, or 404 response
    on error
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
    """ Creates new `Amenity` instance in storage

    Return:
        Empty dictionary and response status 200, or 404 response
    on error
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
    """ Updates `Amenity` instance in storage by id in URI subpath, with
    kwargs from HTTP body request JSON dict

    Args:
        amenity_id: uuid of `Amenity` instance in storage

    Return:
        Empty dictionary and response status 200, or 404 response
    on error
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
