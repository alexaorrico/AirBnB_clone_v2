#!/usr/bin/python3
"""Module containing a Flask Blueprint routes that handles all default
RESTFul API actions for the link between Place objects and Amenity objects"""
from api.v1.views import app_views
from flask import abort, jsonify
from markupsafe import escape
from models import storage
from models.amenity import Amenity
from models.place import Place
from os import getenv


def retrive_object(cls, id):
    """Retrives a resource based on given class and id."""
    obj = storage.get(cls, escape(id))
    if obj is None:
        abort(404)
    return (obj)


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def places_amenities_get(place_id):
    """Returns a list of Amenity for a Place resource of given id"""
    place = retrive_object(Place, place_id)
    amenities = [amenity.to_dict() for amenity in place.amenities]
    return (jsonify(amenities))


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def places_amenities_delete(place_id, amenity_id):
    """Removes an Amenity resource of given id from amenities
    associated with a Place of given id."""
    place = retrive_object(Place, place_id)
    amenity = retrive_object(Amenity, amenity_id)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity.id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity.id)
    # place.save() amenity.save() if updated_at needs to be updated
    storage.save()
    return (jsonify({}))


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def places_amenities_post(place_id, amenity_id):
    """Adds an Amenity of given id in the list of
    amenities associated with a Place of given id."""
    place = retrive_object(Place, place_id)
    amenity = retrive_object(Amenity, amenity_id)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity in place.amenities:
            return (jsonify(amenity.to_dict()))
        place.amenities.append(amenity)
    else:
        if amenity.id in place.amenity_ids:
            return (jsonify(amenity.to_dict()))
        place.amenities = amenity  # setter appends amenity.id to amenity_ids
    # place.save() amenity.save() if updated_at needs to be updated
    storage.save()
    return (jsonify(amenity.to_dict()), 201)
