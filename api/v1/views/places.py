#!/usr/bin/python3
"""View for Place objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_city_places(city_id):
    """return all the places linked to the city with city_id"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """return a place by id in the database"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """delete a place by id in the database"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    place.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """create a place linked to the city with city_id"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    try:
        place_dict = request.get_json()
    except Exception:
        return 'Not a JSON', 400

    if 'user_id' not in place_dict:
        return 'Missing user_id', 400
    elif not storage.get(User, place_dict['user_id']):
        abort(404)
    elif 'name' not in place_dict:
        return 'Missing name', 400

    place_dict['city_id'] = city_id
    new_place = Place(**place_dict)
    new_place.save()
    return jsonify(new_place.to_dict()), 201
