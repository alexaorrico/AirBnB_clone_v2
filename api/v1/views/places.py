#!/usr/bin/python3
"""new view for Places objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort, request
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, {'message': 'Not a JSON'})
    if 'name' not in request.get_json():
        abort(400, {'message': 'Missing name'})
    if 'user_id' not in request.get_json():
        abort(400, {'message': 'Missing user_id'})
    data = request.get_json()
    user = storage.get('User', data['user_id'])
    if user is None:
        abort(404)
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return (jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, {'message': 'Not a JSON'})
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return (jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def placeSearch():
    """This is to retrieves all place objects depending on
    the json in the body request"""
    if not request.is_json:
        abort(400, 'Not a JSON')
