#!/usr/bin/python3
"""RESTful API view to handle actions for 'Amenity' objects related to
a given 'Place' object"""

from flask import abort, request, jsonify

from api.v1.views import app_views
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def place_amenities(place_id):
    """
    GET: Retrieves the list of all Amenity objects of the place where
         id == place_id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST", "DELETE"], strict_slashes=False)
def place_amenities_control(place_id, amenity_id):
    """
    POST: Add Amenity object with id == amenity_id to Place object with
          id == place_id
    DELETE: Remove Amenity object with id == amenity_id from Place object with
          id == place_id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if request.method == "POST":
        response = jsonify(amenity.to_dict())
        if storage_t == "db":
            if amenity in place.amenities:
                return response, 200
            place.amenities.append(amenity)
        else:
            id = amenity.id
            if id in place.amenity_ids:
                return response, 200
            place.amenity_ids.append(id)
        storage.save()
        return response, 201

    elif request.method == "DELETE":
        if storage_t == "db":
            if amenity not in place.amenities:
                abort(404)
            place.amenities.remove(amenity)
        else:
            id = amenity.id
            if id not in place.amenity_ids:
                abort(404)
            place.amenity_ids.remove(id)

        storage.save()
        return jsonify({}), 200
