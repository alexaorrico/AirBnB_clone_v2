#!/usr/bin/python3
"""ALX SE Flask Api Place-Amenity Module."""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity
from models.place import Place
import os


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def get_place_amenities(place_id: str):
    """Return list of all amenities link to a particular place given its id."""
    place: Place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(amenities)
    return jsonify(place.amenity_ids)


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=['DELETE'],
        strict_slashes=False)
def delete_place_amenity(place_id: str, amenity_id: str):
    """Return list of all amenities link to a particular place given its id."""
    place: Place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        for amenity in place.amenities:
            if amenity.id == amenity_id:
                place.amenities.remove(amenity)
                storage.save()
                return jsonify({})
        abort(404)

    if amenity_id in place.amenity_ids:
        amenity: Amenity = storage.get(Amenity, val)
        place.amenity_ids.remove(amenity_id)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=['POST'],
        strict_slashes=False)
def create_place_amenity(place_id: str, amenity_id: str):
    """Create an amenity for a particular place given the place id."""
    place: Place = storage.get(Place, place_id)
    amenity: Amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        for obj in place.amenities:
            if obj.id == amenity_id:
                return jsonify(amenity.to_dict())
        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201

    if amenity_id in place.amenity_ids:
        return jsonify(amenity.to_dict())
    place.amenity_ids.append(amenity_id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
