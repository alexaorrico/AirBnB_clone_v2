#!/usr/bin/python3
"""
a view for City objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State
from models.place import Place


@app_views.route('/cities/<string:city_id>/places', methods=['GET', 'POST'])
def get_add_places(city_id):
    """
    get place information for all places in a specified city otherwise 404
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        places = []
        for place in city.places:
            places.append(place.to_dict())
        return jsonify(places)

    if request.method == 'POST':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        kwargs = request.get_json()
        if 'user_id' not in kwargs:
            return make_response(jsonify({'error': 'Missing user_id'}), 400)
        user = storage.get("User", kwargs['user_id'])
        if user is None:
            abort(404)
        if 'name' not in kwargs:
            return make_response(jsonify({'error': 'Missing name'}), 400)
        kwargs['city_id'] = city_id
        place = place(**kwargs)
        place.save()
        return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['GET', 'DELETE', 'PUT'])
def managePlaces(place_id):
    """
    manipulate place information for specified place
    """
    placeObj = storage.get("Place", place_id)
    if placeObj is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(placeObj.to_dict())

    if request.method == 'DELETE':
        placeObj.delete()
        storage.save()
        return (jsonify({}))

    if request.method == 'PUT':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for attr, val in request.get_json().items():
            if attr not in ['id', 'user_id', 'city_id',
                            'created_at', 'updated_at']:
                setattr(place, attr, val)
        place.save()
        return jsonify(place.to_dict())
