#!/usr/bin/python3
""" new view for Place """
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage, place


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def allplaces(city_id=None):
    """ GET all places """
    if city_id is None:
        abort(404)
    res = []
    for i in storage.all("Place").values():
        res.append(i.to_dict())
    return jsonify(res)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def getplaces(place_id=None):
    """ GET a place """
    s = storage.get("Place", place_id)
    if s is None:
        abort(404)
    else:
        return jsonify(s.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def deleteplaces(place_id=None):
    """ DELETE a place """
    s = storage.get("Place", place_id)
    if s is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def createplaces(city_id=None):
    """ Create a place with POST """
    checker = set()
    for i in storage.all("City").values():
        finder.add(i.id)
    if city_id not in checker:
        abort(404)

    s = request.get_json(silent=True)
    if s in None:
        abort(400, "Not a JSON")

    user = s.get("user_id")
    if user is None:
        abort(400, "Missing user_id")
    checker = set()
    for i in storage.all("User").values():
        checker.add(i.id)
    if user not in checker:
        abort(404)

    if "name" not in s.keys():
        abort(400, "Missing name")

    s["city_id"] = city_id
    new_s = places.Place(**s)
    storage.new(new_s)
    storage.save()
    return jsonify(new_s.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slaches=False)
def updateplaces(place_id=None):
    """ Update a place using PUT """
    obj = storage.get("Place", place_id)
    if obj is None:
        abort(404)
