#!/usr/bin/python3
'''routes for Place objects'''

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.state import State
import json


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    '''Retrieve all Place objects of a City'''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    '''Retrieve a Place object'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    '''Delete a Place object'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    '''Create a Place object'''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif 'user_id' not in data:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    elif 'name' not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    data['city_id'] = city_id
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    place = Place(**data)
    place.save()

    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''Update a Place object'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at',
                       'updated_at']:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    '''Search for places based on JSON request'''
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    states = data.get("states", None)
    cities = data.get("cities", None)
    amenities = data.get("amenities", None)

    places = []

    if not states and not cities and not amenities:
        places = [place.to_dict() for place in storage.all(Place).values()]
    else:
        if states:
            states_obj = [storage.get(State, s_id) for s_id in states]
            for state in states_obj:
                if state:
                    for city in state.cities:
                        if city:
                            for plc in city.places:
                                places.append(plc)
        if cities:
            city_obj = [storage.get(City, c_id) for c_id in cities]
            for city in city_obj:
                if city:
                    for place in city.places:
                        if plc not in places:
                            places.append(plc)
        if amenities:
            if not places:
                places = storage.all(Place).values()
            amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
            places = [place for place in places
                            if all([am in place.amenities
                               for am in amenities_obj])]
    list_of_places = [pl.pop('amenities', None).to_dict() for pl in places]

    return jsonify(list_of_places)
