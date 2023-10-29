#!/usr/bin/python3
"""places view"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_places(city_id):
    """retrieve all places of a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        places_list = []
        for place in city.places:
            places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def a_place(place_id):
    """retrieve a place with its id"""
    try:
        place = storage.get(Place, place_id)
        return jsonify(place.to_dict())
    except Exception:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete a place object"""
    if place_id is None:
        abort(404)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def POST_request_places(city_id):
    """"post request"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if not data:
        return abort(400, {'message': 'Not a JSON'})
    if 'user_id' not in data:
        return abort(400, {'message': 'Missing user_id'})
    user_id = data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if 'name' not in data:
        abort(400)
        return abort(400, {'message': 'Missing name'})
    # creation of a new place
    new_place = Place(**data)
    new_place.city_id = city_id
    new_place.user_id = user_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def PUT_place(place_id):
    """Put request"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if not data:
        return abort(400, {'message': 'Not a JSON'})
    for key, value in data.items():
        if key not in ["id", "user_id", "city_id", "state_id",
                       "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
