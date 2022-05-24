#!/usr/bin/python3
"""
this module creates a new view for the link
between Place objects and Amenity objects
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities',
                 strict_slashes=False, methods=['GET'])
def getAmenityByPlace(place_id):
    """
    returns the list of all Amenity objects of a Place
    """
    place = storage.get(Place, place_id)
    if place:
        if storage_t == 'db':
            result = []
            for amenitie in place.amenities:
                result.append(amenitie.to_dict())
            return jsonify(result), 200
        else:
            listAmenities = [amenitie.to_dict(
                             ) for amenitie in place.amenities]
            return jsonify(listAmenities)
    else:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def deleteAmenityForAPlace(place_id, amenity_id):
    """
    deletes an amenity for a Place
    """
    place = storage.get(Place, place_id)
    amenitie = storage.get(Amenity, amenity_id)
    listId = [amenity.to_dict()['id'] for amenity in place.amenities]
    if place and amenitie and amenity_id in listId:
        if storage_t == 'db':
            place.amenities.remove(amenitie)
            place.save()
            return jsonify({}), 200
        else:
            place.amenity_ids.remove(amenity_id)
            return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST'])
def AddAmenityForAPlace(place_id, amenity_id):
    """
    add an amenity for a Place
    """
    place = storage.get(Place, place_id)
    amenitie = storage.get(Amenity, amenity_id)
    listId = [amenity.to_dict()['id'] for amenity in place.amenities]
    if place and amenitie:
        if amenity_id not in listId:
            if storage_t == 'db':
                place.amenities.append(amenitie)
                storage.save()
                return jsonify(amenitie.to_dict()), 200
            else:
                place.amenity_ids.append(amenity_id)
                return jsonify(amenitie.to_dict()), 200
        else:
            return jsonify(amenitie.to_dict()), 200
    else:
        abort(404)
