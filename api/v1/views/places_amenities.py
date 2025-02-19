#!/usr/bin/python3
"""places maneities module"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv
import sqlalchemy

db = (getenv("HBNB_TYPE_STORAGE"), "json_file")


@app_views.route('/places/<place_id>/amenities')
def place_amenities(place_id=None):
    """GET method for amenities en place"""
    list_amenities = []
    obj_place_am = storage.get("Place", place_id)
    if obj_place_am is None:
        abort(404)
    amenities = obj_place_am.amenities
    for amenity in amenities:
        list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def amenity_review_delete(place_id=None, amenity_id=None):
    """DELETE method for amenities en place"""
    obj_place = storage.get("Place", place_id)
    obj_amenity = storage.get("Amenity", amenity_id)
    if obj_amenity is None:
        abort(404)
    if obj_place is None:
        abort(404)
    amenities = obj_place.amenities
    list_am = [am.id for am in amenities]
    if amenity_id not in list_am:
        abort(404)
    for am in amenities:
        if am.id == amenity_id:
            obj_amenity.delete()
    storage.save()
    return (jsonify({})), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def amenity_place(place_id, amenity_id):
    """POST method for amenities en place"""
    obj_place = storage.get("Place", place_id)
    obj_amenity = storage.get("Amenity", amenity_id)
    if obj_place is None:
        abort(404)
    if obj_amenity is None:
        abort(404)
    list = [item.id for item in obj_place.amenities]
    if obj_amenity.id in list:
        return (jsonify(obj_amenity.to_dict()), 200)
    if db is 'db':
        obj_place.amenities.append(obj_amenity)
    else:
        obj_place.amenities.append(obj_amenity.id)
    return jsonify(obj_amenity.to_dict()), 201
