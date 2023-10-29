#!/usr/bin/python3
"""A host file for a new view for Place objects that handles
all default RESTFul API actions
"""

# Importing modules from system files
from flask import request, jsonify
from werkzeug.exceptions import MethodNotAllowed, NotFound, BadRequest

# Importing modules from project files
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage, storage_t


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def places_handler(city_id=None, place_id=None):
    """A function to handle places' endpoint"""
    handlers = {
            'GET': get_places,
            'POST': add_place,
            'DELETE': remove_place,
            'PUT': update_place
            }
    if request.method in handlers:
        return handlers[request.method](city_id, place_id)
    else:
        return MethodNotAllowed(list(handlers.keys()))


def get_places(city_id=None, place_id=None):
    """A function to retrieve list of all place objects of a city."""
    if city_id:
        city = storage.get(City, city_id)
        if city:
            all_places = []
            if storage_t == 'db':
                all_places = list(city.places)
            else:
                all_places = list(filter(
                    lambda x: x.city_id == city_id,
                    storage.all(Place).values()))
            places = list(map(lambda x: x.to_dict(), all_places))
            return (jsonify(places))

    elif place_id:
        place = storage.get(Place, place_id)
        if place:
            return (jsonify(place.to_dict()))
    else:
        raise NotFound()


def remove_place(city_id=None, place_id=None):
    """A function to delete the place object."""
    if place_id:
        place = storage.get(Place, place_id)
        if place:
            storage.delete(place)
            storage.save()
            return (jsonify({}), 200)
        else:
            raise NotFound()


def add_place(city_id=None, place_id=None):
    """A function to add a place object."""
    city = storage.get(City, city_id)
    if not city:
        raise NotFound()
    data = request.get_json()
    if type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'user_id' not in data:
        raise BadRequest(description='Missing user_id')

    user = storage.get(User, data['user_id'])
    if not user:
        raise NotFound()
    if 'name' not in data:
        raise BadRequest(description='Missing name')

    # If city id is available and linked to city save it in place
    data['city_id'] = city_id
    new_place = Place(**data)
    new_place.save()
    # Returning new place with status code 201
    return jsonify(new_place.to_dict()), 201


def update_place(city_id=None, place_id=None):
    """A function that update the place object."""
    place = storage.get(Place, place_id)
    if not place:
        raise NotFound()

    ignored_keys = ('id', 'user_id', 'city_id', 'created_at', 'updated_at')
    data = request.get_json()
    if type(data) is not dict:
        raise BadRequest(discription='Not a JSON')
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(place, key, value)
    place.save()

    return jsonify(place.to_dict()), 200
