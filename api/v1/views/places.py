#!/usr/bin/python3
""" view for place """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def retrieve_places(city_id):
    """ function to retrieve related places """
    if city_id is None:
        return abort(404)
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    places = city.places
    list_place = []
    for place in places:
        list_place.append(place.to_dict())
    return jsonify(list_place)


@app_views.route('places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ retrieves place by id """
    if place_id is None:
        return abort(404)
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    return jsonify(place.to_dict())


@app_views.route('places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """ function to delete place instance """
    if place_id is None:
        return abort(404)
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """ post a new place """
    if city_id is None:
        return abort(404)
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    if not request.json:
        return 'Not a JSON', 400
    if 'user_id' not in request.json:
        return 'Missing user_id', 400
    user = storage.get(User, request.json.get('user_id'))
    if user is None:
        return abort(404)
    if 'name' not in request.json:
        return 'Missing user_id', 400

    data = request.get_json()
    place = Place(**data)
    place.city_id = city.id
    place.save()
    place_dict = place.to_dict()
    return jsonify(place_dict), 201


@app_views.route('places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ update place instance """
    if place_id is None:
        return abort(404)
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    if not request.json:
        return 'Not a JSON', 400
    body = request.get_json()
    for key, value in body.items():
        if key == 'id' or key == 'created_at' or key == 'updated_at' or\
                key == 'user_id' or key == 'city_id':
            continue
        setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
