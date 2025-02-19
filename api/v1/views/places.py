#!/usr/bin/python3
""" The State Object view
"""

from flask import jsonify, abort, request
from models.place import Place
from models.user import User
from models.city import City
from models import storage
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places(city_id):
    """ Retrieves places linked to a city from storage
    """
    retrieved_places = []
    city = storage.get(City, city_id)
    if city:
        for place in city.places:
            retrieved_places.append(place.to_dict())
        return jsonify(retrieved_places), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place_by_id(place_id):
    """ Retrieves one place from storage based on the id
    """
    try:
        return jsonify(storage.get(Place, place_id).to_dict()), 200
    except Exception:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_by_id(place_id):
    """ Deletes the place from storage by its given id
    """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """ Adds a new user to storage
    """
    city = storage.get(City, city_id)
    if city:
        body = request.get_json()
        if body is None:
            abort(400, 'Not a JSON')
        if 'name' not in body:
            abort(400, 'Missing name')
        if 'user_id' not in body:
            abort(400, 'Missing user_id')
        user_id = storage.get(User, body['user_id'])
        if user_id is None:
            abort(404)
        new_place = Place(**body)
        new_place.city_id = city_id
        new_place.save()
    else:
        abort(404)
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """ Modifies the attributes of a place if they are not dates or id
    """
    place = storage.get(Place, place_id)
    if place:
        body = request.get_json()
        if body is None:
            abort(400, 'Not a JSON')
        for key, value in body.items():
            if key not in ['id', 'user_id', 'city_id',
                           'created_at', 'updated_at']:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
    else:
        abort(404)
