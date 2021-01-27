#!/usr/bin/python3
""" places create  """
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def all_Places(city_id):
    """all Place City ID """
    dic = []
    places = storage.all('Place').items()
    for key, value in places:
        if value.to_dict()['city_id'] == city_id:
            dic.append(value.to_dict())
    return jsonify(dic)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_id(place_id):
    """ Return Place id """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete a Place"""
    place = storage.get(Place, place_id)
    if place:
        place.delete()
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Create a Place, and return their dictionary representation
    if city_id its not found, 404 error return """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    content = request.get_json()
    if content is None:
        abort(400, description='Not a JSON')
    if 'user_id' not in content:
        abort(400, description="Missing user_id")
    elif item_locator(content['user_id'], User) is False:
        abort(404)
    if 'name' not in content:
        abort(400, description="Missing name")
    # if 'city_id' not in kwargs:
    content['city_id'] = city_id
    place = Place(**content)
    # place.city_id = city_id
    storage.new(place)
    storage.save()
    return (jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def upd_place(place_id):
    """Update Place"""
    place = storage.get(Place, place_id)
    ignore_list = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    if not place:
        abort(404)
    json_content = request.get_json()
    if json_content is None:
        abort(400, 'Not a JSON')
    for key, value in json_content.items():
        if key != 'id' and key != 'created_ad' and key != 'updated_at':
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


def item_locator(id, item):
    """items list"""
    if item == User:
        users = storage.all('User').items()
        for key, value in users:
            if value.to_dict()['id'] == id:
                return True
        return False
    if item == Place:
        place = storage.all('Place').items()
        for key, value in place:
            if value.to_dict()['id'] == id:
                return True
        return False
