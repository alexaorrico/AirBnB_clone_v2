#!/usr/bin/python3
"""Module containing a Flask Blueprint routes that handles
all default RESTFul API actions for Place resource"""
from api.v1.views import app_views
from flask import abort, make_response, jsonify, request
from markupsafe import escape
from models import storage
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


def retrive_object(cls, id):
    """Retrive a resource based on given class and id."""
    obj = storage.get(cls, escape(id))
    if obj is None:
        abort(404)
    return (obj)


def validate_request_json(request):
    """Checks validity of request's json content"""
    if not request.is_json:
        abort(make_response(jsonify(error="Not a JSON"), 400))
    req_json = request.get_json()
    if request.method == 'POST' and '/places_search' not in request.base_url:
        if 'user_id' not in req_json:
            abort(make_response(jsonify(error="Missing user_id"), 400))
        retrive_object(User, req_json['user_id'])
        if 'name' not in req_json:
            abort(make_response(jsonify(error="Missing name"), 400))
    return (req_json)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search_get():
    """Returns a list of Place resources based on JSON of request body.
    JSON contain 3 optional keys states, cities and amenities with list of ids.
    If both cities and states list are empty returns all Place objects which
    have all Amenities listed in amenities list. Otherwise, returns all places
    related to each City in every State listed in states list, plus every City
    in cities list, not related to States in states list. Each place in result
    must have all Amenities in amenities list."""
    req_json = validate_request_json(request)
    state_id_list = set(req_json.get('states', []))  # empty or with state ids
    city_id_list = set()
    # add all cities for each state in states list to city_id_list
    for state_id in state_id_list:
        state = storage.get(State, state_id)  # a state or None
        state_cities = state.cities if state else []  # a state's cities or []
        city_id_list.update([city.id for city in state_cities])

    city_id_list.update(req_json.get('cities', []))  # empty or with city ids
    amenity_id_list = set(req_json.get('amenities', []))  # amenity ids or []
    search_result = []  # assuming a place is unique to a city
    if city_id_list:
        for city_id in city_id_list:
            city = storage.get(City, city_id)  # a city or None
            city_places = city.places if city else []  # a citie's places or []
            # search_result.extend(
            #     [place.to_dict() for place in city_places
            #      if amenity_id_list.issubset(
            #          set([amenity.id for amenity in place.amenities]))])
            for place in city_places:
                plce_amnties = set([amenity.id for amenity in place.amenities])
                if amenity_id_list.issubset(plce_amnties):
                    plce_dict = place.to_dict()
    # Due to a bug not found yet, plce_dict contains 'ameneties' key
    # with a value of Amenity objects list
                    plce_dict.pop('amenities', None)
                    search_result.append(plce_dict)
    else:
        # search_result.extend(
        #     [plce.to_dict() for plce in storage.all(Place).values()
        #      if amenity_id_list.issubset(
        #          set([amnty.id for amnty in plce.amenities]))])
        places = storage.all(Place).values()
        for place in places:
            place_amenities = set([amenity.id for amenity in place.amenities])
            if amenity_id_list.issubset(place_amenities):
                plce_dict = place.to_dict()
                plce_dict.pop('amenities', None)
                search_result.append(plce_dict)

    return (jsonify(search_result))


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def cities_places_get(city_id):
    """Returns a list of places for a City resource with given id"""
    city = retrive_object(City, city_id)
    # using newly added City.places getter for filestorage mode
    places = [place.to_dict() for place in city.places]
    return (jsonify(places))


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def places_get(place_id):
    """Returns a Place resource based on given id"""
    place = retrive_object(Place, place_id)
    return (jsonify(place.to_dict()))


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def places_delete(place_id):
    """Deletes a Place resource based on given id"""
    place = retrive_object(Place, place_id)
    storage.delete(place)
    storage.save()
    return (jsonify({}))


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def cities_places_post(city_id):
    """Creates a Place resource in a City of given id
    if request content is valid."""
    city = retrive_object(City, city_id)
    req_json = validate_request_json(request)
    req_json['city_id'] = city.id
    new_place = Place(**req_json)
    new_place.save()
    return (jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def places_put(place_id):
    """Updates a Place resource of given id if request content is valid."""
    place = retrive_object(Place, place_id)
    req_json = validate_request_json(request)
    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in req_json.items():
        if key not in ignore:
            setattr(place, key, value)
    place.save()
    return (jsonify(place.to_dict()))
