#!/usr/bin/python3
"""
Create a new view for Place objects that handles all default RESTFul API
actions
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.user import User
from models.place import Place


# Define a route to search for places based on parameters in the request body
@app_views.route('/places_search',
                 methods=['POST'],
                 strict_slashes=False)
def places_search():
    """
    To Search for place according to parameters
    in body request
    """
    # Check if the request is valid JSON
    if request.is_json:
        body = request.get_json()
    else:
        abort(400, 'Not a JSON')

    place_list = []

    # Search for places based on states
    if 'states' in body:
        for state_id in body['states']:
            state = storage.get(State, state_id)
            if state is not None:
                for city in state.cities:
                    for place in city.places:
                        place_list.append(place)

    # Search for places based on cities
    if 'cities' in body:
        for city_id in body['cities']:
            city = storage.get(City, city_id)
            if city is not None:
                for place in city.places:
                    place_list.append(place)

    # Filter places based on amenities
    if 'amenities' in body and len(body['amenities']) > 0:
        if len(place_list) == 0:
            place_list = [place for place in storage.all(Place).values()]
        del_list = []
        for place in place_list:
            for amenity_id in body['amenities']:
                amenity = storage.get(Amenity, amenity_id)
                if amenity not in place.amenities:
                    del_list.append(place)
                    break
        for place in del_list:
            place_list.remove(place)

    if len(place_list) == 0:
        place_list = [place for place in storage.all(Place).values()]

    place_list = [place.to_dict() for place in place_list]
    for place in place_list:
        try:
            del place['amenities']
        except KeyError:
            pass

    return jsonify(place_list)


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def places_by_city_requests(city_id):
    """
    Perform API requests of places by city
    """
    # To Handle GET requests
    if request.method == 'GET':
        # to retrieve all places related to specific city, if exists
        cities = storage.all(City)
        try:
            key = 'City.' + city_id
            city = cities[key]
            place_list = [place.to_dict() for place in city.places]
            return jsonify(place_list)
        except KeyError:
            abort(404)

    # Handle POST requests to create a new place
    elif request.method == 'POST':
        # create a new place
        cities = storage.all(City)

        if ('City.' + city_id) not in cities.keys():
            abort(404)

        if request.is_json:
            body_request = request.get_json()
        else:
            abort(400, 'Not a JSON')

        # check for required attributes
        if 'name' not in body_request:
            abort(400, 'Missing name')
        if 'user_id' not in body_request:
            abort(400, 'Missing user_id')

        # for the purposes of verifying user_id is valid
        users = storage.all(User)
        if ('User.' + body_request['user_id']) not in users.keys():
            abort(404)

        # Instantiate, store, and return a new Place object
        body_request.update({'city_id': city_id})
        new_place = Place(**body_request)
        storage.new(new_place)
        storage.save()
        return jsonify(new_place.to_dict()), 201

    else:
        abort(501)


# Define a route to handle GET, DELETE, and PUT requests for a specific place
@app_views.route('/places/<place_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place_methods(place_id=None):
    """Perform API requests of on place objects
    """
    # Handle GET requests to retrieve a specific place
    if request.method == 'GET':

        # retrieve specific place object, if exists
        places = storage.all(Place)
        try:
            key = 'Place.' + place_id
            place = places[key]
            return jsonify(place.to_dict())
        except KeyError:
            abort(404)

    # Handle DELETE requests to delete a specific place
    elif request.method == 'DELETE':

        # for deleting specific place, if exists
        places = storage.all(Place)
        try:
            key = 'Place.' + place_id
            storage.delete(places[key])
            storage.save()
            return jsonify({}), 200
        except KeyError:
            abort(404)

    # Handle PUT requests to update a specific place
    elif request.method == 'PUT':
        places = storage.all(Place)
        key = 'Place.' + place_id
        try:
            place = places[key]

            # to convert JSON request to dictionary
            if request.is_json:
                body_request = request.get_json()
            else:
                abort(400, 'Not a JSON')

            # Update Place object attributes based on the JSON data
            ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
            for key, val in body_request.items():
                if key not in ignore:
                    setattr(place, key, val)

            storage.save()
            return jsonify(place.to_dict()), 200

        except KeyError:
            abort(404)
    else:
        abort(501)
