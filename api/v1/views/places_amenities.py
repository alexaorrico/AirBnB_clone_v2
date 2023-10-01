#!/usr/bin/python3
"""
route for handling place and amenities linking
"""
from flask import jsonify, abort
from os import getenv
from models import storage
from api.v1.views import app_views, storage


@app_views.route("/places/<place_id>/amenities",
                 methods=["GET"],
                 strict_slashes=False)
def amenity_by_place(place_id):
    """Get amenities of  a place"""
    fetched_obj = storage.get("Place", str(place_id))

    all_amenities = []

    if fetched_obj is None:
        abort(404)

    for obj in fetched_obj.amenities:
        all_amenities.append(obj.to_dict())

    return jsonify(all_amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity_of_a_place(place_id, amenity_id):
    """REmove link between place and amenity"""
    if not storage.get("Place", str(place_id)):
        abort(404)
    if not storage.get("Amenity", str(amenity_id)):
        abort(404)

    fetched_obj = storage.get("Place", place_id)
    found = 0

    for obj in fetched_obj.amenities:
        if str(obj.id) == amenity_id:
            if getenv("HBNB_TYPE_STORAGE") == "db":
                fetched_obj.amenities.remove(obj)
            else:
                fetched_obj.amenity_ids.remove(obj.id)
            fetched_obj.save()
            found = 1
            break

    if found == 0:
        abort(404)
    else:
        resp = jsonify({})
        resp.status_code = 201
        return resp


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"],
                 strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """Link amenity to place"""
    fetched_obj = storage.get("Place", str(place_id))
    amenity_obj = storage.get("Amenity", str(amenity_id))
    found_amenity = None

    if not fetched_obj or not amenity_obj:
        abort(404)

    for obj in fetched_obj.amenities:
        if str(obj.id) == amenity_id:
            found_amenity = obj
            break

    if found_amenity is not None:
        return jsonify(found_amenity.to_dict())

    if getenv("HBNB_TYPE_STORAGE") == "db":
        fetched_obj.amenities.append(amenity_obj)
    else:
        fetched_obj.amenity_ids.append(str(amenity_obj.id))

    fetched_obj.save()

    resp = jsonify(amenity_obj.to_dict())
    resp.status_code = 201

    return resp
