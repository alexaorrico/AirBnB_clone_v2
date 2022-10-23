#!/usr/bin/python3
"""This module handles amenities route"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views

from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET', 'POST'])
def amenities_route():
    """
    amenities_route handles GET , POST request to the amenities
    route
    """
    if request.method == 'GET':
        amenity = list(map(lambda obj: obj.to_dict(),
                           storage.all(Amenity).values()))
        return make_response(jsonify(amenity), 200)
    elif request.method == 'POST':
        form_data = request.get_json(silent=True)
        if form_data is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'name' not in form_data:
            return make_response(jsonify({'error': 'Missing name'}), 400)
        new_state = Amenity(**form_data)
        new_state.save()
        return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def amenity_route(amenity_id):
    """
    amenity_route handle GET, DELET, PUT request to specific amenity
    :param amenity_id: is the id of the amenity
    """
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)
    if request.method == 'GET':
        return make_response(jsonify(amenity.to_dict()), 200)
    elif request.method == 'DELETE':
        amenity.delete()
        return make_response(jsonify({}), 200)
    elif request.method == 'PUT':
        form_data = request.get_json(silent=True)
        if form_data is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        amenity.update(**form_data)
        return make_response(jsonify(amenity.to_dict()), 200)
