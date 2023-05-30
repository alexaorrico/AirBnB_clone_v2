#!/usr/bin/python3
""" Place - Amenity"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv
import sqlalchemy


db = (getenv("HBNB_TYPE_STORAGE", "json_file"))


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def place_amenities(place_id=None):
    """Get method for amenities and place."""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    if db is 'db':
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get("Amenity", amenity_id).to_dict()
                     for amenity_id in place.amenity_ids]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if not place or not amenity:
        abort(404)

    if db is 'db':
        if amenity in place.amenities:
            place.amenities.remove(amenity)
            storage.save()
        else:
            abort(404)
    else:
        if amenity_id in place.amenity_ids:
            place.amenity_ids.remove(amenity_id)
            storage.save()
        else:
            abort(404)

    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if not place or not amenity:
        abort(404)

    if db is 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenities.append(amenity)
            storage.save()
            return jsonify(amenity.to_dict()), 201
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenity_ids.append(amenity_id)
            storage.save()
            return jsonify(amenity.to_dict()), 201
