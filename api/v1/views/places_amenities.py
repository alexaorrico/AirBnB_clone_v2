#!/usr/bin/python3
"""
Index route
"""

from api.v1.views import app_views
from models import storage
from models.user import User
from models.state import State
from flask import jsonify, request, abort


@app_views.route("/places/<place_id>/amenities", methods=['GET'], strict_slashes=False)
def get_amenities(place_id):
    p_storage = type(storage).__name__
    place = storage.get('Place', place_id)
    if not place:
        abort(404)

    if p_storage == "DBStorage":
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get('Amenity', amenity_id).to_dict()
                    for amenity_id in place.amenity_ids]
    return jsonify(amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=['DELETE'], strict_slashes=False)
def delete_aminity(place_id, amenity_id):
    p_storage = type(storage).__name__
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if p_storage == "DBStorage":
        if amenity in place.amenities:
            place.amenities.remove(amenity)
            if place in amenity.place_amenities:
                amenity.place_amenities.remove(place)
            storage.save()
            return jsonify({}), 200
    else:
        if amenity_id in place.amenity_ids:
            place.amenity_ids.remove(amenity_id)
            storage.save()
            return jsonify({}), 200
        else:
            abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=['POST'], strict_slashes=False)
def get_link_pamenity(place_id, amenity_id):
    p_storage = type(storage).__name__
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if p_storage == "DBStorage":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
        amenity.place_ids.append(place_id)
        place.save()
        amenity.save()
        storage.save()
        return jsonify(amenity.to_dict()), 201
