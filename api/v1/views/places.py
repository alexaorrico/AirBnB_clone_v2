#!/usr/bin/python3
'''places blueprint'''

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage, storage_t
from models.place import Place
from models.state import State
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


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def placesSearch():
    '''retrives all place objects depending on the request body'''
    body = request.get_json()
    if body is None:
        abort(400, 'Not a JSON')
    keys = body.keys()
    if len(body) <= 0\
       or (('states' not in keys or len(body['states']) <= 0) and
       ('cities' not in keys or len(body['cities']) <= 0)):
        if 'amenities' not in keys:
            places = storage.all(Place).values()
            dcts = [pl.to_dict() for pl in places]
            if storage_t == 'db':
                for idx in range(len(dcts)):
                    if 'amenities' in dcts[idx].keys():
                        del dcts[idx]['amenities']
            return jsonify(dcts)
        else:
            places = storage.all(Place).values()
            unwanted = []
            for idx, place in enumerate(places):
                if storage_t == 'db':
                    amens_ids = [m.id for m in place.amenities]
                else:
                    amens_ids = place.amenity_ids
                for amenity_id in body['amenities']:
                    if amenity_id not in amens_ids:
                        unwanted.append(idx)
                        break
            for i in unwanted:
                    del places[i]
            dcts = [pl.to_dict() for pl in places]
            if storage_t == 'db':
                for idx in range(len(dcts)):
                    if 'amenities' in dcts[idx].keys():
                        del dcts[idx]['amenities']
            return jsonify(dcts)

    places = storage.all(Place).values()
    wanted_places = []
    cities = {}

    if 'cities' in keys:
        for cityId in body['cities']:
            cities[cityId] = cityId

    if 'states' in keys:
        for state in storage.all(State).values():
            if state.id in body['states']:
                for city in state.cities:
                    cities[city.id] = city.id

    for place in places:
        if len(cities) > 0:
            if place.city_id in cities:
                wanted_places.append(place)
    unwanted = []
    if 'amenities' in keys:
        for idx, place in enumerate(wanted_places):
            if storage_t == 'db':
                amens_ids = [m.id for m in place.amenities]
            else:
                amens_ids = place.amenity_ids
            for amenity_id in body['amenities']:
                if amenity_id not in amens_ids:
                    unwanted.append(idx)
                    break

    for i in unwanted:
        del wanted_places[i]
    dcts = [pl.to_dict() for pl in wanted_places]
    if storage_t == 'db':
        for idx in range(len(dcts)):
            if 'amenities' in dcts[idx].keys():
                del dcts[idx]['amenities']
    return jsonify(dcts)


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
