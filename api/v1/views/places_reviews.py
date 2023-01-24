#!/usr/bin/python3
""" This module contains the places_amenities view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/places/<place_id>/amenities', methods=['GET', 'POST'],
                    strict_slashes=False)
def handle_place_amenities(place_id):
    """ This function handles the place_amenities route """
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    if request.method == 'GET':
        amenities = place.amenities
        return jsonify([amenity.to_dict() for amenity in amenities])
    elif request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')
        elif 'amenity_id' not in request.json:
            abort(400, 'Missing amenity_id')
        amenity = storage.get('Amenity', request.json['amenity_id'])
        if not amenity:
            abort(404)
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        place.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                    methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def handle_place_amenity(place_id, amenity_id):
    """ This function handles the place_amenity route """
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    amenity = storage.get('Amenity', amenity_id)
    if not amenity:
        abort(404)
    if request.method == 'GET':
        if amenity not in place.amenities:
            abort(404)
        return jsonify(amenity.to_dict())
    elif request.method == 'PUT':
        if amenity not in place.amenities:
            abort(404)
        if not request.json:
            abort(400, 'Not a JSON')
        for key, value in request.json.items():
            if key not in ['id', 'user_id', 'city_id', 'created_at',
                            'updated_at']:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    elif request.method == 'DELETE':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
        place.save()
        return jsonify({}), 200
