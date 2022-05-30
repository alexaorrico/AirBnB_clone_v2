#!/usr/bin/python3
""" Place view """
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route('cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def list_places(city_id):
    """ Retrieves the list of all Place objects of a City """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place(place_id):
    """ Retrieves a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def place_delete(place_id):
    """ Deletes a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def new_place(city_id):
    """ Creates a new Place """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    new_place = request.get_json()
    if not new_place:
        abort(400, 'Not a JSON')
    if 'user_id' not in new_place:
        abort(400, 'Missing user_id')
    if not storage.get(User, new_place['user_id']):
        abort(404)
    if 'name' not in new_place:
        abort(400, 'Missing name')
    new_place['city_id'] = city_id
    place = Place(**new_place)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def place_id_put(place_id):
    """ Updates a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    request_json = request.get_json()
    if not request_json:
        abort(400, 'Not a JSON')
    for key, value in request_json.items():
        if key != 'id' and key != 'user_id' and key != 'city_id' \
                and key != 'created_at' and key != 'updated_at':
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
