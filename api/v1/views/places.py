#!/usr/bin/python
'''places blueprint'''

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'],
                 strict_slashes=False)
def getPlacesInCity(city_id=None):
    '''get all places in a city'''
    if city_id is None:
        abort(404)
    ct = storage.get(City, city_id)
    if ct is None:
        abort(404)

    places = storage.all(Place)
    res = []
    for place in places.values():
        if place.city_id == ct.id:
            res.append(place)

    return jsonify([place.to_dict() for place in res])


@app_views.route('/places/<place_id>',
                 methods=['GET'],
                 strict_slashes=False)
def getPlaceById(place_id=None):
    '''gets place by id'''
    if place_id is None:
        abort(404)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def deletePlace(place_id=None):
    '''deletes a place'''
    if place_id is not None:
        res = storage.get(Place, place_id)
        if res is not None:
            storage.delete(res)
            storage.save()
            return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'],
                 strict_slashes=False)
def postPlace(city_id):
    '''posts a new place'''
    if city_id is None:
        abort(404)
    ct = storage.get(City, city_id)
    if ct is None:
        abort(404)

    body = request.get_json()
    if body is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in body.keys():
        abort(400, 'Missing user_id')

    user = storage.get(User, body['user_id'])
    if user is None:
        abort(404)
    if 'name' not in body.keys():
        abort(400, 'Missing name')

    body['city_id'] = ct.id
    place = Place(**body)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def updatePlace(place_id=None):
    '''updates a user'''
    if place_id is None:
        abort(404)
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)

    body = request.get_json()
    if body is None:
        abort(400, 'Not a JSON')
    for key in body.keys():
        if key not in ['id', 'created_at', 'updated_at', 'city_id', 'user_id']:
            setattr(obj, key, body[key])
    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)
