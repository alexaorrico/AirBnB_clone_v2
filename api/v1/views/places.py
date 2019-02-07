#!/usr/bin/python3
""" prepares data for easier viewing """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import OperationalError


@app_views.route('/places', methods=['GET'])
def get_all_places():
    """ Returns all the places in json """
    places = storage.all('Place').values()
    return jsonify([amen.to_dict() for amen in places])


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def post_place(city_id):
    """ makes a new place """
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    if request.mimetype != 'application/json':
        return jsonify(error="Not a JSON"), 400
    try:
        place_json = request.get_json()
    except BadRequest:
        return jsonify(error="Not a JSON"), 400
    if 'name' not in place_json:
        return jsonify(error="Missing name"), 400
    if 'user_id' not in place_json:
        return jsonify(error="Missing user_id"), 400
    if not storage.get('User', place_json['user_id']):
        abort(404)
    place = Place(**place_json)
    setattr(place, 'city_id', city.id)
    try:
        place.save()
    except OperationalError:
        return jsonify(error="Missing name"), 400
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET'])
def get_one_place(place_id):
    """ Returns specified place obj in json """
    if place_id:
        place = storage.get('place', place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def del_place(place_id):
    """ deletes the specified place """
    if place_id:
        place = storage.get('place', place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>', methods=['PUT'])
def put_place(place_id):
    """ updates an place """
    if place_id:
        place = storage.get('place', place_id)
    if not place:
        abort(404)
    if request.mimetype != 'application/json':
        return jsonify(error="Not a JSON"), 400
    try:
        place_json = request.get_json()
    except BadRequest:
        return jsonify(error="Not a JSON"), 400
    """ remove the unwanted params """
    if place_json.get('id'):
        place_json.pop('id')
    if place_json.get('created_at'):
        place_json.pop('created_at')
    if place_json.get('updated_at'):
        place_json.pop('updated_at')
    for k, v in place_json.items():
        setattr(place, k, v)
    place.save()
    return jsonify(place.to_dict())
