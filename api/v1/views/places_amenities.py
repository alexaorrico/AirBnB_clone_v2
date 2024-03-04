#!/usr/bin/python3
"""
Places Amenities Module
"""

from flask import Flask, Blueprint, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity
from os import getenv

app = Flask(__name__)


@app_views.route('/places/<place_id>/amenities', methods=['GET', 'POST'],
                 strict_slashes=False)
def places_amenities(place_id):
    """Handle GET and POST requests on /places/<place_id>/amenities"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        amenities_list = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(amenities_list)

    if request.method == 'POST':
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            abort(405)

        amenity_id = request.get_json()
        if amenity_id is None:
            return jsonify({"error": "Not a JSON"}), 400

        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)

        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200

        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def place_amenity(place_id, amenity_id):
    """Handle DELETE requests on /places/<place_id>/amenities/<amenity_id>"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        place.amenities.remove(amenity)
        storage.save()
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
        storage.save()

    return jsonify({}), 200
