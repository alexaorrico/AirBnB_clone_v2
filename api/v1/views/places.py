#!/usr/bin/python3
"""Create a new view for State objects that handles all default RestFul API"""


from flask import jsonify, abort, request
from models import storage
from models.place import Place
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def get_places(city_id):
    citylist = []
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    else:
        places = city.places
        for place in places:
            citylist.append(place.to_dict())
        return(jsonify(citylist))


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET'])
def get_place(place_id):
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def create_place(city_id):
    fields = ['name', 'user_id']
    city = storage.get('City', city_id)
    res = request.get_json()
    if city is None:
        abort(404)
    if res is None:
        abort(400, 'Not a JSON')
    for i in fields:
        if i not in res:
            abort(400, 'Missing {}'.format(i))
    user = storage.get('User', res['user_id'])
    if user is None:
        abort(404)
    res['city_id'] = city_id
    newPlace = Place(**res)
    storage.new(newPlace)
    storage.save()
    return jsonify(newPlace.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['PUT'])
def modify_place(place_id):
    res = request.get_json()
    place = storage.get('Place', place_id)
    if res is None:
        abort(400, 'Not a JSON')
    if place is None:
        abort(404)
    for k, v in res.items():
            if (k != 'id' and k != 'created_at' and k != "updated_at"):
                setattr(place, k, v)
    storage.save()
    return jsonify(place.to_dict()), 200
