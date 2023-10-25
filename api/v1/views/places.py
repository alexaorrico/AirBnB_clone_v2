#!/usr/bin/python3
"""api places"""
from flask import abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
import json


@app_views.route('/cities/<id>/places', methods=['GET'])
def get_places(id):
    """retrieves all places by city id object"""
    city = storage.get(City, id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    res = places
    response = make_response(json.dumps(res), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@app_views.route('/places/<id>', methods=['GET'])
def get_place(id):
    """retrieves places object with id"""
    place = storage.get(Place, id)
    if not place:
        abort(404)
    res = place.to_dict()
    response = make_response(json.dumps(res), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@app_views.route('/place/<id>', methods=['DELETE'])
def delete_place(id):
    """delets city with id"""
    place = storage.get(place, id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    res = {}
    response = make_response(json.dumps(res), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


@app_views.route('/cities/<id>/places', methods=['POST'])
def post_place(id):
    """inserts place if its valid json and has correct keys and city id"""
    missingMSG = "Missing name"
    userMissingMsg="Missing user_id"
    city = storage.get(City, id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description=userMissingMsg)
    data = request.get_json()
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if 'name' not in request.get_json():
        abort(400, description=missingMSG)
    data["city_id"] = id
    instObj = Place(**data)
    instObj.save()
    res = instObj.to_dict()
    response = make_response(json.dumps(res), 201)
    response.headers['Content-Type'] = 'application/json'
    return response


@app_views.route('/places/<place_id>', methods=['PUT'])
def put_place(place_id):
    """update a place by id"""
    abortMSG = "Not a JSON"
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description=abortMSG)
    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    res = place.to_dict()
    response = make_response(json.dumps(res), 200)
    response.headers['Content-Type'] = 'application/json'
    return response
