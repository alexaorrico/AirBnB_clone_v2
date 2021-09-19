#!/usr/bin/python3
""" View Place """

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place


@app_views.route("/cities/<id>/places", methods=["GET"])
def placeAll(id):
    """id city retrieve json object with his places"""
    ll = []
    s = storage.all('City').values()
    ss = storage.all('Place').values()
    for v in s:
        if v.id == id:
            for vv in ss:
                if vv.city_id == id:
                    ll.append(vv.to_dict())
    if not ll:
        return abort(404)
    return jsonify(ll)


@app_views.route("/places/<id>", methods=["GET"])
def placeId(id):
    """id place retrieve json object"""
    ll = []
    s = storage.all('Place').values()
    for v in s:
        if v.id == id:
            ll.append(v.to_dict())
    if not ll:
        return abort(404)
    return jsonify(ll)


@app_views.route("/places/<id>", methods=["DELETE"])
def placeDel(id):
    """delete place with id"""
    place = storage.get("Place", id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<id>/places', methods=['POST'])
def placePost(id):
    """ POST a new place"""
    if storage.get("City", id) is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    x = request.get_json()
    if "User." + x["user_id"] not in storage.all("User"):
        abort(404)
    x['city_id'] = str(id)
    if "user_id" not in x:
        return jsonify({"error": "Missing user_id"}), 400
    if "name" not in x:
        return jsonify({"error": "Missing name"}), 400
    s = Place(**x)
    s.save()
    return jsonify(s.to_dict()), 201


@app_views.route('/places/<id>', methods=['PUT'])
def placePut(id):
    """ Update a place object """
    ignore = {"id", "user_id", "city_id", "created_at", "updated_at"}
    place = storage.get("Place", id)
    if place is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    x = request.get_json()
    for k, v in x.items():
        if k not in ignore:
            setattr(place, k, v)
    place.save()
    return jsonify(place.to_dict()), 200
