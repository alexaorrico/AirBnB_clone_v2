#!/usr/bin/python3
"""Script that handles place and amenities linking"""
from flask import jsonify, abort
from os import getenv
from api.v1.views import app_views, storage


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def amenity_by_place(place_id):
    """get all amenities of a place
    Args:
        place_id: amenity id"""
    if not storage.get("Place", str(place_id)):
        abort(404)
    objs = storage.get("Place", str(place_id))
    list_of_amenities = []
    for obj in objs.amenities:
        list_of_amenities.append(obj.to_dict())
    return jsonify(list_of_amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def unlink_amenity_from_place(place_id, amenity_id):
    """unlinks an amenity in a place
    Args:
        place_id: place id
        amenity_id: amenity id"""
    if not storage.get("Place", str(place_id)):
        abort(404)
    if not storage.get("Amenity", str(amenity_id)):
        abort(404)
    objs = storage.get("Place", place_id)
    found = 0
    for obj in objs.amenities:
        if str(obj.id) == amenity_id:
            if getenv("HBNB_TYPE_STORAGE") == "db":
                objs.amenities.remove(obj)
            else:
                objs.amenity_ids.remove(obj.id)
            objs.save()
            found = 1
            break
    if found == 0:
        abort(404)
    else:
        response = jsonify({})
        response.status_code = 200
        return response


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"], strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """links a amenity with a place
    Args:
        place_id: place id
        amenity_id: amenity id"""
    objs = storage.get("Place", str(place_id))
    amenity_object = storage.get("Amenity", str(amenity_id))
    found = None
    if not objs or not amenity_object:
        abort(404)
    for obj in objs.amenities:
        if str(obj.id) == amenity_id:
            found = obj
            break
    if found is not None:
        return jsonify(found.to_dict())
    if getenv("HBNB_TYPE_STORAGE") == "db":
        objs.amenities.append(amenity_object)
    else:
        objs.amenities = amenity_object
    objs.save()
    response = jsonify(amenity_object.to_dict())
    response.status_code = 201
    return response
