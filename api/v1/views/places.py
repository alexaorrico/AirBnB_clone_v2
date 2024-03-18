#!/usr/bin/python3
""" Place objects RESTful API. """
from flask import jsonify, request, abort, current_app
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from api.v1.views import app_views

"""HTTP methods"""
G = 'GET'
P = 'POST'
D = 'DELETE'
Pu = 'PUT'


@app_views.route("/cities/<city_id>/places", methods=[G], strict_slashes=False)
def get_places(city_id):
    """API endpoint that delivers all Place objects in a city"""
    checked_city = storage.get(City, city_id)
    if not checked_city:
        abort(404)
    list_of_places = [place.to_dict() for place in checked_city.places]
    return jsonify(list_of_places)


@app_views.route("/cities/<city_id>/places", methods=[P], strict_slashes=False)
def create_place(city_id):
    """API endpoint that creates a new Place object in a city"""
    current_app.logger.info(city_id)
    checked_city = storage.get(City, city_id)
    if not checked_city:
        current_app.logger.info("checked city not found")
        abort(404)
    HTTP_body = request.get_json(silent=True)
    current_app.logger.info(HTTP_body)
    if not HTTP_body:
        abort(400, 'Not a JSON')
    if 'user_id' not in HTTP_body:
        abort(400, 'Missing user_id')
    checked_user = storage.get(User, HTTP_body['user_id'])
    if not checked_user:
        abort(404)
    if 'name' not in HTTP_body:
        abort(400, 'Missing name')
    if 'city_id' not in HTTP_body:
        HTTP_body['city_id'] = city_id
    latest_place = Place(**HTTP_body)
    storage.new(latest_place)
    storage.save()
    return jsonify(latest_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=[G], strict_slashes=False)
def get_place(place_id):
    """API endpoint that delivers a specific Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=[D], strict_slashes=False)
def delete_place(place_id):
    """API endpoint that deletes a specific Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>", methods=[Pu], strict_slashes=False)
def update_place(place_id):
    """API endpoint that updates a specific Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    HTTP_body = request.get_json(silent=True)
    if not HTTP_body:
        abort(400, 'Not a JSON')
    ignoring_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in HTTP_body.items():
        if key not in ignoring_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
