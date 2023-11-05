#!/usr/bin/python3
'''places.py'''
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from os import getenv
import requests
import json


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id=None):
    '''get places by city'''
    city = storage.get(City, city_id)
    if city:
        places = []
        for place in city.places:
            places.append(place.to_dict())
        return jsonify(places)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id=None):
    '''get place'''
    if place_id:
        place = storage.get(Place, place_id)
        if place:
            return jsonify(place.to_dict())
        else:
            abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id=None):
    '''delete place'''
    place = storage.get(Place, place_id)
    if place:
        place.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id=None):
    '''post place'''
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in request.get_json():
        return jsonify({'error': 'Missing user_id'}), 400
    if 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    user = storage.get(User, request.get_json()['user_id'])
    if not user:
        abort(404)
    city = storage.get(City, city_id)
    if city:
        place = Place(**request.get_json())
        place.city_id = city.id
        place.save()
        return jsonify(place.to_dict()), 201
    abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id=None):
    '''UPdate place'''
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    place = storage.get(Place, place_id)
    if place:
        (request.get_json()).pop('id', None)
        (request.get_json()).pop('updated_at', None)
        (request.get_json()).pop('created_at', None)
        (request.get_json()).pop('city_id', None)
        (request.get_json()).pop('user_id', None)
        for key, value in request.get_json().items():
            setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def post_places_search():
    '''post place_search'''

    req_body = request.get_json()

    if req_body is None:
        return jsonify({'error': 'Not a JSON'}), 400

    if req_body == {} or (req_body.get('states') is None and
                          req_body.get('cities') is None and
                          req_body.get('amenities') is None):
        places = storage.all(Place)
        return jsonify([place.to_dict() for place in places.values()])

    filtered_places = []

    if req_body.get('states'):
        state_obj = []
        for state_id in req_body.get('states'):
            state = storage.get(State, state_id)
            if state:
                state_obj.append(state)

        for state in state_obj:
            for city in state.cities:
                for place in city.places:
                    filtered_places.append(place)

    if req_body.get('cities'):
        city_obj = []
        for city_id in req_body.get('cities'):
            city = storage.get(City, city_id)
            if city:
                city_obj.append(city)

        for city in city_obj:
            for place in city.places:
                if place not in filtered_places:
                    filtered_places.append(place)

    if not filtered_places:
        places = storage.all(Place)
        filtered_places = [place for place in places.values()]

    if req_body.get('amenities'):
        amenities_obj = []
        HBNB_API_PORT = getenv('HBNB_API_PORT')

        port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
        url = "http://0.0.0.0:{}/api/v1/places/".format(port)

        for amenity_id in req_body.get('amenities'):
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                amenities_obj.append(amenity)

        removed_places = []
        for place in filtered_places:
            place_api = url + '{}/amenities'
            req = place_api.format(place.id)
            response = requests.get(req)
            places_obj = json.loads(response.text)

            amity_id_list = [storage.get(Amenity, amenity['id'])
                             for amenity in places_obj]

            for amenity in amenities_obj:
                if amenity not in amity_id_list:
                    removed_places.append(place)
                    break

        for place in removed_places:
            filtered_places.remove(place)

    return jsonify([place.to_dict() for place in filtered_places])
