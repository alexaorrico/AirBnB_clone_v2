#!/usr/bin/python3
"""place flask triggers"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<string:city_id>/places',
                 methods=['GET'], strict_slashes=False)
def placesobj(city_id):
    """retrieves a place object"""
    placeobj = storage.get(City, city_id)
    if placeobj is None:
        abort(404)
    listplaces = []
    for place in placeobj.places:
        listplaces.append(place.to_dict())
    return jsonify(listplaces)


@app_views.route('/places/<string:place_id>',
                 methods=['GET'], strict_slashes=False)
def placeobj1(place_id):
    placeobj = storage.get(Place, place_id)
    if placeobj is None:
        abort(404)
    return jsonify(placeobj.to_dict())


@app_views.route('/places/<string:place_id>',
                 methods=['DELETE'], strict_slashes=False)
def deleteplace(place_id):
    """deletes a place object"""
    placeobj = storage.get(Place, place_id)
    if placeobj is None:
        abort(404)
    storage.delete(placeobj)
    storage.save()
    return (jsonify({}))


@app_views.route('/cities/<string:city_id>/places',
                 methods=['POST'], strict_slashes=False)
def createplace(city_id):
    """Creates a place"""
    cityplace = storage.get(City, city_id)
    if cityplace is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    jsonfile = request.get_json()
    if 'user_id' not in jsonfile:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    userid = storage.get(User, jsonfile['user_id'])
    if userid is None:
        abort(404)
    if 'name' not in jsonfile:
        return make_response(jsonify({"error": "Missing name"}), 400)
    jsonfile['city_id'] = city_id
    jsonplace = Place(**jsonfile)
    jsonplace.save()
    return make_response(jsonify(jsonplace.to_dict()), 201)


@app_views.route('/places/<string:place_id>',
                 methods=['PUT'], strict_slashes=False)
def updateplace(place_id):
    """update a place as json"""
    updateplace = storage.get(Place, place_id)
    if updateplace is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(updateplace, key, value)
    updateplace.save()
    return (jsonify(updateplace.to_dict()))
