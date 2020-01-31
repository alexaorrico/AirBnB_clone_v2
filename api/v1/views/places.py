#!/usr/bin/python3
"""
module for place views
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places(city_id):
    """ Retrieves the list of all City's places objects """
    cities = storage.all("City")
    response = []
    for key in cities.keys():
        if key.split('.')[-1] == city_id:
            list_places = cities.get(key).places
            for place in list_places:
                response.append(place.to_dict())
            return jsonify(response)
    abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieves a Place object """
    places = storage.all("Place")
    for key in places.keys():
        if key.split('.')[-1] == place_id:
            return jsonify(places.get(key).to_dict())
    abort(404)


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object """
    places = storage.all("Place")
    for key in places.keys():
        if key.split('.')[-1] == place_id:
            storage.delete(places.get(key))
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """ Creates a Place """
    dic = request.get_json()
    if not dic:
        abort(400, "Not a JSON")
    if not ('user_id' in dic.keys()):
        abort(400, "Missing user_id")
    if not ('name' in dic.keys()):
        abort(400, "Missing name")
    cities = storage.all('City')
    for key in cities.keys():
        if key.split('.')[-1] == city_id:
            users = storage.all('User')
            for k in users.keys():
                if k.split('.')[-1] == dic.get('user_id'):
                    place = Place(city_id=city_id, **dic)
                    place.save()
                    return jsonify(place.to_dict()), 201
    abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """ Updates a Place object """
    places = storage.all("Place")
    place = None
    for key in places.keys():
        if key.split('.')[-1] == place_id:
            place = places.get(key)
    if not place:
        abort(404)
    new_dict = request.get_json()
    if not new_dict:
        abort(400, "Not a JSON")
    for key, value in new_dict.items():
        if key in ('id', 'created_at', 'updated_at'):
            continue
        else:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
