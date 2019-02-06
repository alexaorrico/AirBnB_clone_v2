#!/usr/bin/python3
""" City view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.state import City



@app_views.route('/states/<state_id>/cities', strict_slashes=False, methods=['GET', 'POST'])
def our_cities(state_id=None):
    """ retrieves all cities in a state """

    try:
        obj = storage.all("State").pop("State." + state_id)
    except KeyError:
        abort(404)

    if request.method == 'GET':
        my_cities = [city.to_dict() for city in obj.cities]
        return (jsonify(my_cities))

    if request.method == 'POST':
        try:
            data = request.get_json()
        except:
            return (jsonify('Not a JSON'), 400)

        if "name" not in data.keys():
            return (jsonify("Missing name"), 400)
        city = City(**data)
        city.state_id = state_id
        storage.new(city)
        storage.save()
        return (jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET', 'DELETE', 'PUT'])
def my_city(city_id=None):
    """ retrieves a city object """
    try:
        obj = storage.all("City").pop("City." + city_id)
    except KeyError:
        abort(404)

    if request.method == 'GET':
        return (jsonify(obj.to_dict()))

    if request.method == 'DELETE':
        storage.delete(obj)
        storage.save()
        return (jsonify({}), 200)

    if request.method == 'PUT':
        try:
            data = request.get_json()
        except:
            return (jsonify('Not a JSON'), 400)
        for k, v in data.items():
            if k not in ['id', 'created_at', 'updated_at', 'state_id']:
                setattr(obj, k, v)
        storage.new(obj)
        storage.save()
        return (jsonify(obj.to_dict()), 200)
