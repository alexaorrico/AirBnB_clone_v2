#!/usr/bin/python3
""" A new view for the link between Place and Amenity objects
that handles all default RESTFul API actions.
"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def place_amenities(place_id):
    """ Retrieves the list of all Amenity objects of a Place. """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if getenv("HBNB_TYPE_STORAGE") == 'db':
        list_amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        list_amenities = [storage.get(Amenity, amenity_id).to_dict()
                          for amenity_id in place.amenity_ids]

    return jsonify(list_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'], strict_slashes=False)
def place_amenities_id(place_id, amenity_id):
    """ Deletes or links an Amenity object to a Place. """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if request.method == 'DELETE':
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            if amenity not in place.amenities:
                abort(404)
            place.amenities.remove(amenity)
        else:
            if amenity_id not in place.amenity_ids:
                abort(404)
            place.amenity_ids.remove(amenity_id)

        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'POST':
        if getenv("HBNB_TYPE_STORAGE") == 'db':
            if amenity not in place.amenities:
                place.amenities.append(amenity)
            else:
                return make_response(jsonify(amenity.to_dict()), 200)
        else:
            if amenity_id not in place.amenity_ids:
                place.amenity_ids.append(amenity_id)
            else:
                return make_response(jsonify(amenity.to_dict()), 200)

        storage.save()
        return make_response(jsonify(amenity.to_dict()), 201)
