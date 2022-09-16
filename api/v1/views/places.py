#!/usr/bin/python3
"""Module with the view for Place objects"""
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from flask import request, abort
import json


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def places(city_id):
    """Return a list of dictionaries of all places in a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        places = []
        for city in city.places:
            places.append(city.to_dict())
        return json.dumps(places, indent=4)
    try:
        data = request.get_json()
    except Exception:
        return 'Not a JSON', 400
    if 'user_id' not in data.keys():
        return 'Missing user_id', 400
    user = storage.get(User, data.get('user_id'))
    if user is None:
        abort(404)
    if 'name' not in data.keys():
        return 'Missing name', 400
    data['city_id'] = city_id
    new_place = Place(**data)
    new_place.save()
    return json.dumps(new_place.to_dict(), indent=4), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_place(place_id):
    """Get a place instance from the storage"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        return json.dumps(place.to_dict(), indent=4)
    if request.method == 'DELETE':
        place.delete()
        storage.save()
        return {}
    if request.method == 'PUT':
        try:
            data = request.get_json()
        except Exception:
            return 'Not a JSON', 400
        for k, v in data.items():
            if k != 'id' or k != 'city_id' or k != 'user_id'\
               or k != 'created_at' or k != 'updated_at':
                setattr(place, k, v)
        storage.save()
        return json.dumps(place.to_dict(), indent=4), 200
