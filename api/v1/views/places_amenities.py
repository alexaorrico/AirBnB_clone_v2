#!/usr/bin/python3
"""
handles all default RESTFul API actions
"""


from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET', 'POST', 'DELETE'])
def handle_place_amenities(place_id):
    """handles all default RESTFul API actions"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        amenities = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(amenities)

    if request.method == 'POST':
        amenity_id = request.get_json()
        if amenity_id is None:
            abort(400, 'Not a JSON')

        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)

        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200

        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201

    if request.method == 'DELETE':
        amenity_id = request.get_json()
        if amenity_id is None:
            abort(400, 'Not a JSON')

        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)

        if amenity not in place.amenities:
            abort(404)

        place.amenities.remove(amenity)
        storage.save()
        return jsonify({}), 200
