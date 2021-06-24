#!/usr/bin/python3
""" Module to handle places RESTful API actions """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def all_places(city_id):
    places = storage.all(Place).values()
    cities = storage.all(City).values()
    users = storage.all(User).values()

    place = [place for place in places if place.city_id == city_id]

    city = [city for city in cities if city.id == city_id]
    if len(city) == 0:
        abort(404)

    if request.method == 'GET':
        return jsonify(list(map(lambda x: x.to_dict(), place)))

    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')
        if 'name' not in request.json:
            abort(400, 'Missing name')
        if 'user_id' not in request.json:
            abort(400, 'Missing user_id')
        new_dict = request.get_json()
        user = [user for user in users if user.id == new_dict['user_id']]
        if len(user) == 0:
            abort(404)
        new_dict['city_id'] = city_id
        obj = Place(**new_dict)
        storage.new(obj)
        storage.save()
        return jsonify(obj.to_dict()), 201

@app_views.route('/places/<place_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def one_place(place_id):
    places = storage.all(Place).values()
    place = [place for place in places if place.id == place_id]
    if len(place) == 0:
        abort(404)

    if request.method == 'GET':
        return place[0].to_dict()

    if request.method == 'PUT':
        if not request.json:
            abort(400, 'Not a JSON')
        for k, v in request.get_json().items():
            if k not in ('id', 'created_at', 'updated_at', 'user_id', 'city_id'):
                setattr(place[0], k, v)
        storage.save()
        return jsonify(place[0].to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(place[0])
        storage.save()
        return {}, 200
