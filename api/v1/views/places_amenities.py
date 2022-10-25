#!/usr/bin/python3
""" view for place_amenity objects """

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenity(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    amenity_dict = []
    for amenity in place.amenities:
        amenity_dict.append(amenity.to_dict())
    return jsonify(amenity_dict)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_place(amenity_id):
    """Deletes a Amenity object to a Place"""
    try:
        amenity = storage.get(Amenity, amenity_id)
        place = storage.get(Place, place_id)
        if amenity.place_id != place_id:
            abort(404)
        amenity.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    except KeyError:
        abort(404)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenity_place(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    try:
        place = storage.get(Place, place_id)
        data = request.get_json()
        if data.get("name") is None:
            return make_response(jsonify({"error": "Missing name"}), 400)
        if data.get("user_id") is None:
            return make_response(jsonify({"error": "Missing user_id"}), 400)
        data["place_id"] = place_id
        amenity = Amenity(**data)
        amenity.save()
        response = jsonify(amenity.to_dict())
        return make_response(response, 201)
    except KeyError:
        abort(404)
    except Exception:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
