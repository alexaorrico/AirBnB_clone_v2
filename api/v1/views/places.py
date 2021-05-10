#!/usr/bin/python3
"""Places"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage, place
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def getallplaces(city_id=None):
    """Gets all places"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    res = []
    for i in city.places:
        res.append(i.to_dict())
    return jsonify(res)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def getplaces(place_id=None):
    """Gets a place"""
    s = storage.get(Place, place_id)
    if s is None:
        abort(404)
    else:
        return jsonify(s.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteplaces(place_id=None):
    """Deletes a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        place.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def createplaces(city_id=None):
    """Create a place"""
    city = storage.get("City", city_id)
    print("HERE")
    if city is None:
        abort(404)
    print("found it")
    content = request.get_json(silent=True)
    if content is None:
        jsonify("Not a JSON"), 400
    elif 'name' not in content:
        jsonify("Missing name"), 400
    elif 'user_id' not in content:
        jsonify("Missing user_id"), 400
    content["city_id"] = city_id
    u_id = content['user_id']
    if storage.get("User", u_id):
        new_s = Place(**content)
        new_s.save()
        return jsonify(new_s.to_dict()), 201
    abort(404)

@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def updateplaces(place_id=None):
    """Update a place"""
    obj = storage.get("Place", place_id)
    if obj is None:
        abort(404)

    s = request.get_json(silent=True)
    if s is None:
        return jsonify("Not a JSON"), 400
    else:
        for k, v in s.items():
            if k in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
                pass
            else:
                setattr(obj, k, v)
        storage.save()
        res = obj.to_dict()
        return jsonify(res), 200
