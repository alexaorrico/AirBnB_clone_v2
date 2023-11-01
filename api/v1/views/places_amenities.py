#!/usr/bin/python3
"""adding and removing amenities using place_id & amenity_id"""

from flask import jsonify, request, abort
from . import Amenity, app_views, Place, storage
import os


@app_views.route("/places/<place_id>/amenities", strict_slashes=False)
def get_amenit_place(place_id):
    """Displays place info for a given ID and returns list of place objects"""
    amenit_place = storage.get(Place, str(place_id))
    if amenit_place is None:
        abort(404, description="Not found")
    return jsonify([list.to_dict() for list in amenit_place.amenities])


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST", "DELETE"], strict_slashes=False)
def delete_amenit_place(amenity_id, place_id):
    """Removes amenit_place using amenity_id and place_id"""
    amenit_place = storage.get(Place, str(place_id))
    deleted_amenity_place = storage.get(Amenity, str(amenity_id))
    if amenit_place is None or deleted_amenity_place is None:
        abort(404, description="Not found")
    storage_type = os.getenv("HBNB_TYPE_STORAGE", None)
    if request.method == "DELETE":
        if deleted_amenity_place not in amenit_place.amenities:
            abort(404, description="Not found")
        if storage_type == "db":
            amenit_place.amenities.remove(deleted_amenity_place)
        else:
            amenit_place.amenity_ids.remove(deleted_amenity_place.id)
        storage.save()
        return jsonify({})
    else:
        if deleted_amenity_place in amenit_place.amenities:
            return jsonify({})
        if storage_type == "db":
            amenit_place.amenities.append(deleted_amenity_place)
        else:
            amenit_place.amenity_ids.append(deleted_amenity_place.id)
        storage.save()
        return jsonify(deleted_amenity_place.to_dict()), 201
