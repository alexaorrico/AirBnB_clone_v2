#!/usr/bin/python3
""" State objects RESTFul API. """
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Retrieves list of all Amenity objs. """
    amenities = storage.all(Amenity).values()
    list_of_amenities = [amenity.to_dict() for amenity in amenities]
    return jsonify(list_of_amenities)


@app_views.route('/amenities/<a_id>', methods=['GET'], strict_slashes=False)
def get_amenity(a_id):
    """ Returns a amenity based from it's ID. """
    amenity = storage.get(Amenity, a_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<a_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(a_id):
    """ Deletes amenity based on id. """
    amenity = storage.get(Amenity, a_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def creates_amenity():
    """ Create an Amenity object. """
    HTTP_body = request.get_json(silent=True)
    if not HTTP_body:
        abort(400, 'Not a JSON')
    if 'name' not in HTTP_body:
        abort(400, 'Missing name')
    latest_amenity = Amenity(**HTTP_body)
    storage.new(latest_amenity)
    storage.save()
    return jsonify(latest_amenity.to_dict()), 201


@app_views.route('/amenities/<a_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(a_id):
    """ Updating a amenity obj. """
    amenity = storage.get(Amenity, a_id)
    if not amenity:
        abort(404)
    HTTP_body = request.get_json(silent=True)
    if not HTTP_body:
        abort(400, 'Not a JSON')
    ignoring_keys = ['id', 'created_at', 'updated_at']
    for key, value in HTTP_body.items():
        if key not in ignoring_keys:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
