#!/usr/bin/python3
"""This is the module for the Place view"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/api/v1/cities/<city_id>/places',
                 strict_slashes=False,
                 methods=['GET', 'POST']
                 )
def places_by_city(city_id):
    """This method retrive and create place(s) in a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404, 'Not found')

    if request.method == 'GET':
        places = [place.to_dict() for place in city.places]
        return jsonify(places)

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if 'user_id' not in data:
            abort(400, 'Missing user_d')
        user = storage.get(User, data['user_id'])
        if not user:
            abort(404)
        if 'name' not in data:
            return abort(400, 'Missing name')
        data['city_id'] = city_id
        place = Place(**data)
        place.save()
        return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def modify_place(place_id):
    """This method modifies the place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())


    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify(), 200

    if request.method == 'PUT':
        data = request.json_get()
        if not data:
            abort(400, 'Not a JSON')

        atrr = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for k, v in data.items():
            if k not in attr:
                setattr(place, k, v)
        storage.save()
        return jsonify(place.to_dict()), 200

