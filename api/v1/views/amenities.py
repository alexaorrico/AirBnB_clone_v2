#!/usr/bin/python3
""" amenities RESTfull API handler """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    """ get all amenities """
    my_list = []
    amenities = storage.all("Amenity")
    for amenity in amenities.values():
        my_list.append(amenity.to_dict())
    return jsonify(my_list)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """get amenity by id"""
    try:
        return jsonify(storage.get("Amenity", amenity_id).to_dict())
    except:
        abort(404)


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """delete amenity by id"""
    try:
        my_amenity = storage.get("Amenity", amenity_id)
        my_amenity.delete()
        return {}, 200
    except:
        abort(404)


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """creates a new amenity"""
    try:
        return {}, 200
    except:
        abort(404)
