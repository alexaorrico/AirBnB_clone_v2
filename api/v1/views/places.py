#!/usr/bin/python3
""" Flask routes for `Place` object related URI subpaths using the
`app_views` Blueprint.
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def GET_all_Place(city_id):
    """ Returns JSON list of all `Place` instances associated
    with a given `City` instance in storage

    Return:
        JSON list of all `Place` instances for a given `City` instance
    """
    city = storage.get(City, city_id)

    if city:
        place_list = []
        for place in city.places:
            place_list.append(place.to_dict())
        return jsonify(place_list)
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=['GET'],
                 strict_slashes=False)
def GET_Place(place_id):
    """ Returns `Place` instance in storage by id in URI subpath

    Args:
        place_id: uuid of `Place` instance in storage

    Return:
        `Place` instance with corresponding uuid, or 404 response
    on error
    """
    place = storage.get(Place, place_id)

    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def DELETE_Place(place_id):
    """ Deletes `Place` instance in storage by id in URI subpath

    Args:
        place_id: uuid of `Place` instance in storage

    Return:
        Empty dictionary and response status 200, or 404 response
    on error
    """
    place = storage.get(Place, place_id)

    if place:
        storage.delete(place)
        storage.save()
        return ({})
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def POST_Place(city_id):
    """ Creates new `Place` instance in storage

    Return:
        Empty dictionary and response status 200, or 404 response
    on error
    """
    city = storage.get(City, city_id)

    if city:
        req_dict = request.get_json()
        if not req_dict:
            return (jsonify({'error': 'Not a JSON'}), 400)
        elif 'name' not in req_dict:
            return (jsonify({'error': 'Missing name'}), 400)
        elif 'user_id' not in req_dict:
            return (jsonify({'error': 'Missing user_id'}), 400)
        name = req_dict.get('name')
        user_id = req_dict.get('user_id')
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        new_Place = Place(name=name, city_id=city_id, user_id=user_id)
        new_Place.save()

        return (jsonify(new_Place.to_dict()), 201)
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=['PUT'],
                 strict_slashes=False)
def PUT_Place(place_id):
    """ Updates `Place` instance in storage by id in URI subpath, with
    kwargs from HTTP body request JSON dict

    Args:
        place_id: uuid of `Place` instance in storage

    Return:
        Empty dictionary and response status 200, or 404 response
    on error
    """
    place = storage.get(Place, place_id)
    req_dict = request.get_json()

    if place:
        if not req_dict:
            return (jsonify({'error': 'Not a JSON'}), 400)
        for key, value in req_dict.items():
            if key not in ['id', 'created_at', 'updated_at',
                           'user_id', 'city_id']:
                setattr(place, key, value)
        storage.save()
        return (jsonify(place.to_dict()))
    else:
        abort(404)
