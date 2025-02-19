#!/usr/bin/python3
"""
Module defines a view for Amenity instances
Place has many Amenities
"""

from api.v1.views.__init__ import app_views
from flask import abort, jsonify
from models import storage
from os import getenv
from models.place import Place
from models.amenity import Amenity

storage_type = getenv('HBNB_TYPE_STORAGE')


@app_views.route("/places/<place_id>/amenities", methods=['GET'],
                 strict_slashes=False)
def place_to_amenity_index(place_id):
    """
    Retrieves list of Amenity objects of a Place object on
    GET /api/v1/places/<place_id>/amenities
    """
    parent_obj = storage.get(Place, place_id)
    if parent_obj is None:
        abort(404)
    else:
        if storage_type == 'db':
            place_amenities_raw = parent_obj.amenities
            place_amenities = [
                amenity.to_dict() for amenity in place_amenities_raw
            ]
            return jsonify(place_amenities)

        elif storage_type == 'file':
            place_amenities_ids = parent_obj.amenities
            place_amenities = []
            all_amenities_dict = storage.all(Amenity)
            all_amenities_keys = list(all_amenities_dict.keys()).sort()
            for amenity_key in all_amenities_keys:
                if all_amenities_dict(amenity_key).id in place_amenities_ids:
                    place_amenities.append(
                        all_amenities_dict(amenity_key).to_dict())
            return jsonify(place_amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """
    Deletes an Amenity object to a place on
    DELETE /api/v1/places/<place_id>/amenities/<amenity_id> request
    """
    parent_obj = storage.get(Place, place_id)
    if parent_obj is None:
        abort(404)
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)
    else:
        if storage_type == 'db':
            place_amenities_raw = parent_obj.amenities
            place_amenities_ids = [
                amenity.id for amenity in place_amenities_raw
            ]
            if amenity_id not in place_amenities_ids:
                abort(404)
            else:
                parent_obj.amenities.remove(amenity_obj)
                storage.save()
                return jsonify({}), 200

        elif storage_type == 'file':
            place_amenities_ids = parent_obj.amenities
            if amenity_id not in place_amenities_ids:
                abort(404)
            else:
                parent_obj.amenities.remove(amenity_id)
                storage.save()
                return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=['POST'],
                 strict_slashes=False)
def post_amenity_on_place(place_id, amenity_id):
    """
    Links an Amenity object to a Place object on
    POST /api/v1/places/<place_id>/amenities/<amenity_id>
    """
    parent_obj = storage.get(Place, place_id)
    if parent_obj is None:
        abort(404)
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)
    else:
        if storage_type == 'file':
            place_amenities_ids = parent_obj.amenities
            if amenity_id in place_amenities_ids:
                return jsonify(amenity_obj.to_dict()), 200
            parent_obj.amenities.append(amenity_id)
            storage.save()
            return jsonify(amenity_obj.to_dict()), 201
        elif storage_type == 'db':
            place_amenities_raw = parent_obj.amenities
            place_amenities_ids = [
                amenity.id for amenity in place_amenities_raw
            ]
            if amenity_id in place_amenities_ids:
                return jsonify(amenity_obj.to_dict()), 200
            parent_obj.amenities.append(amenity_obj)
            storage.save()
            return jsonify(amenity_obj.to_dict()), 201
