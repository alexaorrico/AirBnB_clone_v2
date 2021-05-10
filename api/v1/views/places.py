#!/usr/bin/python3
""" Places routes handler """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from api.v1.views.cities import get_all
from api.v1.views.places_amenities import do_get_amenities
import json


def check(cls, place_id):
    """
        If the place_id is not linked to any Place object, raise a 404 error
    """
    try:
        get_place = storage.get(cls, place_id)
        get_place.to_dict()
    except Exception:
        abort(404)
    return get_place


def get_places(city_id, place_id):
    """
       Retrieves the list of all Place objects
       if place_id is not none get a Place object
    """
    if (place_id is not None):
        get_place = check(Place, place_id).to_dict()
        return jsonify(get_place)
    my_city = storage.get(City, city_id)
    try:
        all_places = my_city.places
    except Exception:
        abort(404)
    places = []
    for c in all_places:
        places.append(c.to_dict())
    return jsonify(places)


def delete_place(place_id):
    """
        Deletes a Place object
        Return: an empty dictionary with the status code 200
    """
    get_place = check(Place, place_id)
    storage.delete(get_place)
    storage.save()
    response = {}
    return jsonify(response)


def create_place(request, city_id):
    """
        Creates a place object
        Return: new place object
    """
    check(City, city_id)
    body_request = request.get_json()
    if (body_request is None):
        abort(400, 'Not a JSON')
    try:
        user_id = body_request['user_id']
    except KeyError:
        abort(400, 'Missing user_id')
    check(User, user_id)
    try:
        place_name = body_request['name']
    except KeyError:
        abort(400, 'Missing name')
    new_place = Place(name=place_name, city_id=city_id, user_id=user_id)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict())


def update_place(place_id, request):
    """
        Updates a Place object
    """
    get_place = check(Place, place_id)
    body_request = request.get_json()
    if (body_request is None):
        abort(400, 'Not a JSON')
    for k, v in body_request.items():
        if (k not in ('id', 'created_at', 'updated_at')):
            setattr(get_place, k, v)
    storage.save()
    return jsonify(get_place.to_dict())


def search(request):
    """
    retrieves all Place objects depending of the JSON
    in the body of the request
    """
    body_request = request.get_json()
    if body_request is None:
        abort(400, 'Not a JSON')
    places_list = []
    places_amenity_list = []
    place_amenities = []
    all_cities = []
    states = body_request.get('states')
    cities = body_request.get('cities')
    amenities = body_request.get('amenities')
    if len(body_request) == 0 or (states is None and cities is None):
        places = storage.all(Place)
        for p in places.values():
            places_list.append(p.to_dict())
    if states is not None and len(states) is not 0:
        for id in states:
            get_cities = get_all(id, None).json
            for city in get_cities:
                all_cities.append(city.get('id'))
        for id in all_cities:
            places = do_get_places(id, None)
            for p in places.json:
                places_list.append(p)
    if cities is not None and len(cities) is not 0:
        for id in cities:
            places = do_get_places(id, None)
            for p in places.json:
                places_list.append(p)
    if amenities is not None and len(amenities) is not 0:
        for p in places_list:
            place_id = p.get('id')
            get_amenities = storage.get(Place, place_id)
            amenity_id = get_amenities.amenities
            for a in amenity_id:
                place_amenities.append(a.id)
                if (a.id in amenities):
                    places_amenity_list.append(p)
            place_amenities = []
        return jsonify(places_amenity_list)

    return jsonify(places_list)


@app_views.route('/cities/<city_id>/places/', methods=['GET', 'POST'],
                 defaults={'place_id': None}, strict_slashes=False)
@app_views.route('/places/<place_id>', defaults={'city_id': None},
                 methods=['GET', 'DELETE', 'PUT'])
def places(city_id, place_id):
    """
        Handle places requests with needed functions
    """
    if (request.method == "GET"):
        return get_places(city_id, place_id)
    elif (request.method == "DELETE"):
        return delete_place(place_id)
    elif (request.method == "POST"):
        return create_place(request, city_id), 201
    elif (request.method == "PUT"):
        return update_place(place_id, request), 200


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def places_search():
    """
    retrieves all Place objects depending of the JSON
    in the body of the request
    """
    return search(request)
