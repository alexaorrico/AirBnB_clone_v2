#!/usr/bin/python3
"""Create a new view for State objects that handles all default RESTFul API
actions"""

from api.v1.views import app_views
from flask import request, abort, jsonify
from models.place import Place
from models.user import User
from models.city import City
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def placeWithId(city_id=None):
    """Methods that retrieves all methods for states with id"""
    if request.method == 'GET':
        """Retrieves get method for all place"""
        for city in storage.all(City).values():
            if city.id == city_id:
                place_list = []
                for place in city.places:
                    place_list.append(place.to_dict())
                return jsonify(place_list)
        return abort(404)

    if request.method == 'POST':
        """Create a new place"""
        cityId = storage.get(City, city_id)
        if cityId is None:
            return abort(404)
        r = request.get_json()
        if r is None:
            abort(400, 'Not a JSON')
        if r.get('user_id') is None:
            abort(400, "Missing user_id")
        user = storage.get(User, r['user_id'])
        if user is None:
            return abort(404)
        if r.get("name") is None:
            abort(400, "Missing name")
        r['city_id'] = city_id
        new = Place(**r)
        new.save()
        return jsonify(new.to_dict()), 201


@app_views.route('/places/<places_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def placesId(places_id):
    """Methods that retrieves all methods for place without id"""
    placeId = storage.get(Place, places_id)
    if placeId is None:
        return abort(404)

    if request.method == 'GET':
        """Retrieves a place of a given place_id"""
        return jsonify(placeId.to_dict())

    if request.method == 'DELETE':
        """Deletes a place of a given place_id"""
        placeId.delete()
        storage.save()
        return jsonify({})

    if request.method == 'PUT':
        """Update an place of a given place_id"""
        r = request.get_json()
        if r is None:
            return abort(400, 'Not a JSON')
        toIgnore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in r.items():
            if key not in toIgnore:
                setattr(placeId, key, value)
        placeId.save()
        return jsonify(placeId.to_dict())
