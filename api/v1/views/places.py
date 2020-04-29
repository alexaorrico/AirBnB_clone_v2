#!/usr/bin/python3
""" All Users """
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=['GET'], strict_slashes=False)
def all_Places(city_id):
    """ return all Place on a City ID 
    if not found, error 404 """
    dic = []
    if item_locator(city_id, 'City') is False:
        abort(404)
    places = storage.all('Place').items()
    for key, value in places:
        if value.to_dict()['city_id'] == city_id:
            dic.append(value.to_dict())
    return jsonify(dic)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_id(place_id):
    """ Return a Place id 
    or Return 404 if it not found """
    place = storage.get('Place', place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """ Delete a Place with their ID, return a void dictionary,
    if place not found, return 404 status"""
    place = storage.get('Place', place_id)
    if place:
        place.delete()
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """ Create a Place """
    if not (request.is_json):
        abort(400, "Not a JSON")
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    if 'user_id' not in request.json:
        abort(400, "Missing user_id")
    if 'name' not in request.json:
        abort(400, "Missing name")
    kwargs = request.get_json()
    if not item_locator(kwargs['user_id'], 'User'):
        abort(404)
    place = Place(**kwargs)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def upd_place(place_id):
    """ Update Place ID, method PUT"""
    place = storage.get('Place', place_id)
    print("--> {}".format(place))
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
    """ fin into items list """
    list_items = storage.all(str(item)).items()
    for key, value in list_items:
        if value.to_dict()['id']== id:
            return True
    return False
