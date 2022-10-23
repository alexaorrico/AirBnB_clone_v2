#!/usr/bin/python3
"""This module handles places routes"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views

from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def places_route(city_id):
    """

    places_route handles get, post request to places
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        places = list(map(lambda obj: obj.to_dict(),
                      city.places))
        return make_response(jsonify(places), 200)
    elif request.method == 'POST':
        form_data = request.get_json(silent=True)
        if form_data is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        required_info = ['user_id', 'name']
        for info in required_info:
            if info not in form_data:
                return make_response(
                    jsonify({'error': 'Missing {}'.format(info)}), 400)
        user = storage.get(User, form_data.get('user_id'))
        if user is None:
            abort(404)
        new_place = Place(city_id=city_id, **form_data)
        new_place.save()
        return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def place_route(place_id):
    """
    place_route handles get, put and delete request to a specific
    place

    :param  place_id: is the id of the place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        return make_response(jsonify(place.to_dict()), 200)
    elif request.method == 'DELETE':
        place.delete()
        return make_response(jsonify({}), 200)
    elif request.method == 'PUT':
        form_data = request.get_json(silent=True)
        if form_data is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        place.update(**form_data)
        return make_response(jsonify(place.to_dict()), 200)
