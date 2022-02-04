#!/usr/bin/python3
'''Contains the places view for the API.'''
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_places(city_id=None, place_id=None):
    '''The method handler for the places endpoint.
    '''
    handlers = {
        'GET': get_places,
        'DELETE': remove_place,
        'POST': add_place,
        'PUT': update_place,
    }
    if request.method in handlers:
        return handlers[request.method](city_id, place_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_places(city_id=None, place_id=None):
    '''Gets the place with the given id or all places in
    the city with the given id.
    '''
    if city_id:
        city = storage.get(City, city_id)
        if city:
            all_places = city.places
            all_places = list(map(lambda x: x.to_dict(), all_places))
            return jsonify(all_places)
    elif place_id:
        place = storage.get(Place, place_id)
        if place:
            return jsonify(place.to_dict())
    raise NotFound()


def remove_place(city_id=None, place_id=None):
    '''Removes a place with the given id.
    '''
    if place_id:
        place = storage.get(Place, place_id)
        if place:
            storage.delete(place)
            storage.save()
            return jsonify({}), 200
    raise NotFound()


def add_place(city_id=None, place_id=None):
    '''Adds a new place.
    '''
    city = storage.get(City, city_id)
    if not city:
        raise NotFound()
    data = request.get_json()
    if data is None or type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'user_id' not in data:
        raise BadRequest(description='Missing user_id')
    city = storage.get(City, data['user'])
    if not city:
        raise NotFound()
    if 'name' not in data:
        raise BadRequest(description='Missing name')
    setattr(data, 'city_id', city_id)
    new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


def update_place(city_id=None, place_id=None):
    '''Updates the place with the given id.
    '''
    xkeys = ('id', 'user_id', 'city_id', 'created_at', 'updated_at')
    if place_id:
        old_place = storage.get(Place, place_id)
        if old_place:
            data = request.get_json()
            if data is None or type(data) is not dict:
                raise BadRequest(description='Not a JSON')
            for key, value in data.items():
                if key not in xkeys:
                    setattr(old_place, key, value)
            old_place.save()
            return jsonify(old_place.to_dict()), 200
    raise NotFound()


@app_views.route('/places_search', methods=['POST'])
def find_places():
    '''Finds places based on a list of State, City, or Amenity ids.
    '''
    data = request.get_json()
    if data is None or type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    places = []
    places_id = []
    keys_status = (
        'states' in data and data['states'],
        'cities' in data and data['cities'],
        'amenities' in data and data['amenities'],
    )
    if keys_status[0]:
        for state_id in data['states']:
            state = storage.get(State, state_id)
            if not state:
                continue
            for city in state.cities:
                new_places = list(
                    filter(lambda x: x.id not in places_id, city.places)
                )
                places.extend(new_places)
                places_id.extend(list((map(lambda x: x.id, new_places))))
    if keys_status[1]:
        for city_id in data['cities']:
            city = storage.get(City, city_id)
            if city:
                new_places = list(
                    filter(lambda x: x.id not in places_id, city.places)
                )
                places.extend(new_places)
    del places_id
    if not any(keys_status) or data is None or type(data) is not dict:
        places = storage.all(Place).values()
    if keys_status[2]:
        amenity_ids = []
        for amenity_id in data['amenities']:
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                amenity_ids.push(amenity.id)
        del_indices = []
        for place in places:
            place_amenities_ids = list(map(lambda x: x.id, place.amenities))
            for amenity_id in amenity_ids:
                if amenity_id not in place_amenities_ids:
                    del_indices.push(place.id)
                    break
        places = list(filter(lambda x: x.id not in del_indices, places))
    places = list(map(lambda x: x.to_dict(), places))
    return jsonify(places), 200
