#!/usr/bin/python3
"""This is the flask file to modify place amenity links"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.user import User
from models.review import Review
from models.amenity import Amenity
from models import storage_t


@app_views.route('/places/<place_id>/amenities',
                 strict_slashes=False, methods=['GET'])
def show_place_amenity(place_id):
    """This method shows all amenities for a place
    """
    place = storage.get("Place", place_id)
    if place:
        return (jsonify([amenity.to_dict() for amenity in place.amenities]))
    else:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """This method deletes a place amenity relationship
    """
    p = storage.get("Place", place_id)
    a = storage.get("Amenity", amenity_id)
    if (p is None or a is None):
        abort(404)
    if (a not in p.amenities):
        abort(404)
    if (storage_t == 'db'):
        p.amenities.remove(a)
    else:
        p.amenity_ids.remove(amenity_id)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST'])
def create_amenity(place_id, amenity_id):
    """This method creates a new review
    """
    p = storage.get("Place", place_id)
    a = storage.get("Amenity", amenity_id)
    if (p is None or a is None):
        abort(404)
    if (a in p.amenities):
        return (jsonify(a.to_dict()), 200)
    if (storage_t == 'db'):
        p.amenities.append(a)
    else:
        p.amenity_ids.append(amenity_id)
    storage.save()
    return (jsonify(a.to_dict()), 201)
