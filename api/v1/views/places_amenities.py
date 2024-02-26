#!/usr/bin/python3
"""
Route for handling the linking between places and amenities
"""
from flask import jsonify, abort
from os import getenv
from api.v1.views import app_views, storage


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def get_amenities_by_place(place_id):
    """
    Retrieves all amenities of a place.
    :param place_id: ID of the place
    :return: JSON of all amenities
    """
    obj_place = storage.get("Place", str(place_id))

    if obj_place is None:
        abort(404)

    all_amenities = []

    for obj in obj_place.amenities:
        all_amenities.append(obj.to_json())

    return jsonify(all_amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def unlink_amenity_from_place(place_id, amenity_id):
    """
    Unlinks an amenity from a place.
    :param place_id: ID of the place
    :param amenity_id: ID of the amenity
    :return: Empty dictionary with 201, or 404 if not found
    """
    if not storage.get("Place", str(place_id)):
        abort(404)
    if not storage.get("Amenity", str(amenity_id)):
        abort(404)

    fetched_obj = storage.get("Place", place_id)
    found = 0

    for obj in obj_place.amenities:
        if str(obj.id) == amenity_id:
            if getenv("HBNB_TYPE_STORAGE") == "db":
                obj_place.amenities.remove(obj)
            else:
                obj_place.amenities = obj_amenity
            obj_place.save()
            found = True
            break

    if not found:
        abort(404)

    return jsonify({}), 201


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"],
                 strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """
    Links an amenity with a place.
    :param place_id: ID of the place
    :param amenity_id: ID of the amenity
    :return: JSON of the added Amenity object, or 404 if not found
    """
    obj_place = storage.get("Place", str(place_id))
    obj_amenity = storage.get("Amenity", str(amenity_id))

    if not obj_place or not obj_amenity:
        abort(404)

    for obj in obj_place.amenities:
        if str(obj.id) == amenity_id:
            return jsonify(obj.to_json())

    if getenv("HBNB_TYPE_STORAGE") == "db":
        obj_place.amenities.append(obj_amenity)
    else:
        obj_place.amenities = obj_amenity

    obj_place.save()

    rsponse = jsonify(obj_amenity.to_json())
    rsponse.status_code = 201

    return rsponse
