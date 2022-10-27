#!/usr/bin/python3
""" New view for places object that handles all
default RESTFul API actions. """
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def handle_place_id(place_id):
    """ Retrieves, updates or deletes a place object given its id. """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        req_data = request.get_json()
        if not req_data:
            abort(400, description='Not a JSON')

        ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

        for key, value in req_data.items():
            if key not in ignore_keys:
                setattr(place, key, value)

        storage.save()
        return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def city_places(city_id):
    """ Retrieves all Place objects of a city and creates
    a new place object in a city given the city's id.
    Returns 404 error if id is not found.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == 'GET':
        list_places = [place.to_dict() for place in city.places]

        return jsonify(list_places)

    if request.method == 'POST':
        req_data = request.get_json()
        if not req_data:
            abort(400, description='Not a JSON')

        if "user_id" not in req_data:
            abort(400, description="Missing user_id")

        user = storage.get(User, req_data['user_id'])
        if not user:
            abort(404)

        if "name" not in req_data:
            abort(400, description="Missing name")

        req_data['city_id'] = city_id
        place = Place(**req_data)
        place.save()
        return make_response(jsonify(place.to_dict()), 201)
@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending of the JSON in the body
    of the request
    """

    if request.get_json() is None:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)

    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    list_places = []
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]

    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return jsonify(places)
