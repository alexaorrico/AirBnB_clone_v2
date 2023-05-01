#!/usr/bin/python3

""" Handles all restful API actions for State"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities',
                 methods=['GET'], strict_slashes=False)
def get_all_amennities():
    """ Returns all amenities """

    amenity_objs = storage.all(Amenity)
    amenities = [obj.to_dict() for obj in amenity_objs.values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_individual_amenites(amenity_id):
    """" Returns indivuidual amenities by id """
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes individual amenities by id """
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    """ Delete the state """
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Creates a new amenity by using the URL """

    my_dict = request.get_json()

    if my_dict is None:
        abort(400, 'Not a JSON')
    if my_dict.get("name") is None:
        abort(400, 'Missing name')

    new_amenity = Amenity(**my_dict)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates an amenity by City ID """
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    my_dict = request.get_json()

    if my_dict is None:
        abort(400, 'Not a JSON')

    amenity.name = my_dict.get("name")
    amenity.save()
    return jsonify(amenity.to_dict()), 200
