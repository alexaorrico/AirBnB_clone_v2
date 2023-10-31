#!/usr/bin/python3
"""Flask route for review model"""

from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from models import storage
from models.amenity import Amenity
from models.place import Place
from os import environ
STOR_TYPE = environ.get('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def place_amenities(place_id=None):
    """route to return all amenities"""

    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404, 'Not found')

    if request.method == "GET":
        amenities_dict = storage.all(Amenity)
        amenities_list = []
        if STOR_TYPE == "db":
            for amenity in place_obj.amenities:
                amenities_list.append(amenity.to_dict())
        else:
            for amenity_id in place_obj.amenity_ids:
                amenities_list.append(storage.get(
                    Amenity, amenity_id).to_dict())
        return jsonify(amenities_list)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=[
    "DELETE"
    ])
def delete_amenity(place_id, amenity_id):
    """Deletes amenity with place id and amenity id"""
    place_obj = storage.get(Place, place_id)

    if place_obj is None:
        abort(404, "Not found")

    amenity_obj = storage.get(Amenity, amenity_id)

    if amenity_obj is None:
        abort(404, "Not found")

    if STOR_TYPE == "db":
        if amenity_obj not in place_obj.amenities:
            abort(404)
        place_obj.amenities.remove(amenity_obj)
    else:
        if amenity_id not in place_obj.amenity_ids:
            abort(404)
        place_obj.amenity_ids.remove(amenity_id)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"])
def create_amenity(place_id, amenity_id):
    """Creates amentity for a place using the place id"""
    place_obj = storage.get(Place, place_id)

    if place_obj is None:
        abort(404, "Not found")

    amenity_obj = storage.get(Amenity, amenity_id)

    if amenity_obj is None:
        abort(404, "Not found")

    if STOR_TYPE == "db":
        if amenity_obj not in place_obj.amenities:
            place_obj.amenities.append(amenity_obj)
        else:
            return make_response(jsonify(amenity_obj.to_dict()), 200)
    else:
        if amenity_id not in place_obj.amenity_ids:
            place_obj.amenity_ids.append(amenity_id)
        else:
            return make_response(jsonify(amenity_obj.to_dict(), 200))
    storage.save()
    return make_response(jsonify(amenity_obj.to_dict()), 201)
