#!/usr/bin/python3
"""Creates a view for Place_amenity"""

from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from flask import abort, request, jsonify

if storage_t == 'db':
    from models.place import place_amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def getAllPlaceAmenity(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def deletePlaceAmenity(place_id, amenity_id):
    """Deletes a Amenity object ot a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    found = None
    for a in place.amenities:
        if a.id == amenity.id:
            found = True
            break
    if found is None:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def linkAmenityPlace(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    found = False
    for a in place.amenities:
        if a.id == amenity.id:
            found = True
            break
    if found:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
