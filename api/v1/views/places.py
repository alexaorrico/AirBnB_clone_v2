#!/usr/bin/python3
""" View for Places """

from flask import jsonify, abort, request, make_response
from models.city import City
from models.place import Place
from api.v1.views import app_views
from models import storage
from sqlalchemy.exc import IntegrityError


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'],
                 strict_slashes=False)
def get_city_places(city_id):
    """ Retrieves the list of all Place objects for a specific City """
    cities_dict = storage.all(City)
    places_list = None
    return_list = []
    for city in cities_dict.values():
        if city.id == city_id:
            places_list = city.places
    if places_list is None:
        abort(404)
    for place in places_list:
        return_list.append(place.to_dict())
    return jsonify(return_list)


@app_views.route('/places/<place_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """ Retrieves a specific Place object by its ID """
    place = storage.get(Place, place_id)
    if place is not None:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a specific Place object by its ID """
    place = storage.get(Place, place_id)
    if place is not None:
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Creates a new Place object for a specific City """
    try:
        request_dict = request.get_json(silent=True)
        if request_dict is not None:
            if 'user_id' not in request_dict.keys():
                return make_response(
                    jsonify({"error": "Missing user_id"}), 400)
            if 'name' in request_dict.keys():
                request_dict['city_id'] = city_id
                new_place = Place(**request_dict)
                new_place.save()
                return make_response(jsonify(new_place.to_dict()), 201)
            return make_response(jsonify({'error': 'Missing name'}), 400)
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    except IntegrityError:
        abort(404)


@app_views.route('/places/<place_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ Updates a specific Place object by its ID """
    request_dict = request.get_json(silent=True)
    if request_dict is not None:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        for key, val in request_dict.items():
            if key not in ['id', 'user_id', 'place_id',
                           'created_at', 'updated_at']:
                setattr(place, key, val)
        storage.save()
        return make_response(jsonify(place.to_dict()), 200)
    return make_response(jsonify({"error": "Not a JSON"}), 400)
