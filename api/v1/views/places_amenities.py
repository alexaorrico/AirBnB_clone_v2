#!/usr/bin/python3
"""view for the link between Place objects and Amenity objects
that hanldes all default RESTFul API actions"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from flask import jsonify
from flask import make_response


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def getPlaceAmenities(place_id):
    """retrieve the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)

    if not place:
        return make_response(jsonify({"error": "Not found"}), 404)
    amenities_list = [amenity.to_dict() for amenity in place.amenities]

    return make_response(jsonify(amenities_list))


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def createPlaceAmenity(place_id, amenity_id):
    """links Amenity object to a Place object"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if not place or not amenity:
        return make_response(jsonify({"error": "Not found"}), 404)

    if amenity in place.amenities:
        return make_response(jsonify(amenity.to_dict()), 200)

    place.amenities.append(amenity)
    storage.save()

    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def deletePlaceAmenity(place_id, amenity_id):
    """delete Amenity object to a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if not place or not amenity:
        return make_response(jsonify({"error": "Not found"}), 404)
    if amenity not in place.amenities:
        return make_response(jsonify({"error": "Not found"}), 404)

    place.amenities.remove(amenity)
    storage.save()

    return make_response(jsonify({}), 200)
