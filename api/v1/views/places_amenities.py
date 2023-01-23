#!/usr/bin/python3
"""
place_amenities view routes
"""
from flask import abort, jsonify

from api.v1.views import app_views
from models import storage, storage_t
from models.amenity import Amenity
from models.place import Place


@app_views.route("/places/<place_id>/amenities", strict_slashes=False)
def place_amenities(place_id):
    """Handles /places/<place_id>/amenities endpoint

    Returns:
        json: list of all amenities of a place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if storage_t == "db":
        amenities = place.amenities
    else:
        amenities = [storage.get(Amenity, id) for id in place.amenity_ids]

    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    methods=["DELETE"],
    strict_slashes=False,
)
def delete_place_amenity(place_id, amenity_id):
    """Handles /places/<place_id>/amenities/<amenity_id> endpoint

    Returns:
        json: empty dict for DELETE or 404
    """
    place, amenity = get_place_and_amenity(place_id, amenity_id)

    if storage_t == "db":
        result = filter(lambda item: item.id == amenity.id, place.amenities)
        if next(result, None) is None:
            abort(404)
        place.amenities.remove(amenity)
    else:
        result = filter(lambda id: id == amenity.id, place.amenity_ids)
        if next(result, None) is None:
            abort(404)
        place.amenity_ids.remove(amenity.id)

    storage.save()
    return jsonify({})


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    methods=["POST"],
    strict_slashes=False,
)
def link_amenity(place_id, amenity_id):
    """Handles /places/<place_id>/amenities/<amenity_id> endpoint

    Returns:
        json: linked aminity object or 404
    """
    place, amenity = get_place_and_amenity(place_id, amenity_id)

    if storage_t == "db":
        result = filter(lambda item: item.id == amenity.id, place.amenities)
        if next(result, None) is None:
            place.amenities.append(amenity)
    else:
        result = filter(lambda id: id == amenity.id, place.amenity_ids)
        if next(result, None) is None:
            place.amenity_ids.append(amenity.id)

    storage.save()
    return jsonify(**amenity.to_dict())


def get_place_and_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    return place, amenity
