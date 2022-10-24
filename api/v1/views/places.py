#!/usr/bin/python3
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
