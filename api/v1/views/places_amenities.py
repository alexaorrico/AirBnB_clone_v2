#!/usr/bin/python3
""" amenities view class """
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review
from models.amenity import Amenity
from flask import jsonify, request, abort, make_response
import os


@app_views.route("/places/<string:place_id>/amenities",
                 strict_slashes=False, methods=["GET"])
def get_amenities_from_place(place_id=None):
    """ retrives all amenities from a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        return jsonify([amenity.to_dict() for amenity in place.amenities])
    else:
        return jsonify([amenity.to_dict() for amenity in place.amenities])


@app_views.route("/places/<string:place_id>/amenities/<string:amenity_id>",
                 strict_slashes=False, methods=["DELETE", "POST"])
def dev_get_amenity_id(amenity_id=None, place_id=None):
    """ gets amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    place = storage.get(Place, place_id)
    if amenity is None or place is None:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    if request.method == "DELETE":
        if os.getenv("HBNB_TYPE_STORAGE") == "db":
            place.amenities.remove(amenity)
            storage.save()
            return jsonify({})

    if request.method == "POST":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict())
        else:
            place.amenities.append(amenity)
            place.save()
            return make_response(jsonify(amenity.to_dict()), 201)
