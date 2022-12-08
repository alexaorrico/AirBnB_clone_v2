#!/usr/bin/python3
""" Method HTTP for Place """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id):
    """ Function that retrieves the places of a city """
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)

    all_places = []
    for place in city.places:
        all_places.append(place.to_dict())
    return jsonify(all_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Function that retrieves a place """
    place = storage.get(Place, place_id)
    return abort(404) if place is None else jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Function that deletes a Place """
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """ Function that create a Place """
    dico = request.get_json()

    city = storage.get(City, city_id)
    if city is None:
        return abort(404)

    if dico is None:
        abort(400, "Not a JSON")

    if dico.get("user_id") is None:
        abort(400, "Missing user_id")

    user_id = storage.get(User, dico['user_id'])
    if user_id is None:
        return abort(404)

    if dico.get("name") is None:
        abort(400, "Missing name")

    dico['city_id'] = city_id
    new_place = Place(**dico)
    new_place.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """ Function that update a Place """
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)

    dico = request.get_json()

    if dico is None:
        abort(400, "Not a JSON")

    for key, value in dico.items():
        if key not in ['id', 'created_at', 'user_id', 'city_id', 'updated_at']:
            setattr(place, key, value)
    place.save()

    return jsonify(place.to_dict()), 200
