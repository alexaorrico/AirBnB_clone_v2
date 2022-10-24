#!/usr/bin/python3
<<<<<<< HEAD
'''contains place routes'''
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def place_by_city(city_id):
    '''fetches places using city id'''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places_list = [p.to_dict() for p in city.places]
    return jsonify(places_list), 200


@app_views.route('/places/<place_id>', methods=['GET'])
def place_by_id(place_id):
    '''fetch place using its id'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    '''DELETE place using its id'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    '''create new place'''
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    elif 'user_id' not in request.get_json():
        return jsonify({'error': 'Missing user_id'}), 400
    else:
        obj_data = request.get_json()
        city = storage.get(City, city_id)
        user = storage.get(User, obj_data['user_id'])
        if city is None or user is None:
            abort(404)
        obj_data['city_id'] = city.id
        obj_data['user_id'] = user.id
        obj = Place(**obj_data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    '''update existing place object'''
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400

    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    obj_data = request.get_json()
    ignore = ('id', 'user_id', 'created_at', 'updated_at')
    for k, v in obj_data.items():
        if k not in ignore:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict()), 200
=======
""" Places """

from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage, place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def getallplaces(city_id=None):
    """Gets all places"""
    if city_id is None:
        abort(404)

    req = []
    for x in storage.all("Place").values():
        req.append(x.to_dict())

    return jsonify(req)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def getplaces(place_id=None):
    """Gets a place"""
    p = storage.get("Place", place_id)
    if p is None:
        abort(404)
    else:
        return jsonify(p.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteplaces(place_id=None):
    """Deletes a place"""
    p = storage.get("Place", place_id)
    if p is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def createplaces(city_id=None):
    """Create a place"""
    checker = set()
    for x in storage.all("City").values():
        finder.add(x.id)
    if city_id not in checker:
        abort(404)

    p = request.get_json(silent=True)
    if p is None:
        abort(400, "Not a JSON")

    user = p.get("user_id")
    if user is None:
        abort(400, "Missing user_id")
    checker = set()
    for x in storage.all("User").values():
        checker.add(x.id)
    if user not in checker:
        abort(404)

    if "name" not in s.keys():
        abort(400, "Missing name")

    p["city_id"] = city_id
    new_p = places.Place(**s)
    storage.new(new_p)
    storage.save()
    return jsonify(new_p.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def updateplaces(place_id=None):
    """Update a place"""
    obj = storage.get("Place", place_id)
    if obj is None:
        abort(404)

    p = request.get_json(silent=True)
    if p is None:
        abort(400, "Not a JSON")
    else:
        for x, y in p.items():
            if x in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
                pass
            else:
                setattr(obj, x, y)
        storage.save()
        res = obj.to_dict()
        return jsonify(req), 200
>>>>>>> c02c8bf79a11e249678224b436b61ec738225fff
