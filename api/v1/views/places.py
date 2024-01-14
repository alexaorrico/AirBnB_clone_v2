#!/usr/bin/python3
"""places.py"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Create a new place"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    kwgs = request.get_json()
    if 'user_id' not in kwgs:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get("User", kwgs['user_id'])
    if user is None:
        abort(404)
    if 'name' not in kwgs:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    kwgs['city_id'] = city_id
    place = Place(**kwgs)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """Update a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'user_id', 'city_id', 'created_at',
                        'updated_at']:
            setattr(place, attr, val)
    place.save()
    return jsonify(place.to_dict())


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def place_search():
    """retrieves all Place objects depending of the JSON
    in the body of the request."""
    body = request.get_json()
    if not body:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    places = storage.all('Place').values()
    if not len(places):
        return jsonify([])
    if not len(body) or not len([x for x in body if len(body[x])]):
        return jsonify([x.to_dict() for x in places])

    result = []
    state_ids = body['states'] if body.get('states') else []
    city_ids = body['cities'] if body.get('cities') else []
    amenity_ids = body['amenities'] if body.get('amenities') else []

    cities = []
    if len(state_ids):
        all_states = storage.all('State').values()
        states = [x for x in all_states if x.id in state_ids]
        for state in states:
            cities.extend(state.cities)
    if len(city_ids):
        all_cities = storage.all('City').values()
        _cities = [x for x in all_cities if x.id in city_ids]
        _cities = [x for x in _cities if x not in cities]
        cities.extend(_cities)

    amenities = []
    if len(amenity_ids):
        all_amenities = storage.all('Amenity').values()
        amenities = [x for x in all_amenities if x.id in amenity_ids]

    for place in places:
        place_amenities = place.amenities
        if place.city_id in [x.id for x in cities]:
            if all(x in place_amenities for x in amenities):
                result.append(place.to_dict())

    return jsonify(result)
