#!/usr/bin/python3
"""Defines views for place operations in the API."""
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

from api.v1.views import app_views
from models import storage, storage_t
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def places_ctrl(city_id=None, place_id=None):
    """Handles place-related API requests."""
    actions = {
        'GET': fetch_all_or_single_place,
        'DELETE': delete_specific_place,
        'POST': create_new_place,
        'PUT': update_existing_place
    }
    if request.method in actions:
        return actions[request.method](city_id, place_id)
    else:
        raise MethodNotAllowed(list(actions.keys()))


def fetch_all_or_single_place(city_id=None, place_id=None):
    """Fetches places based on city or specific place ID."""
    if city_id:
        city = storage.get(City, city_id)
        if city:
            places_list = (list(city.places) if storage_t == 'db' else
                           [place for place in storage.all(Place).values()
                            if place.city_id == city_id])
            place_dicts = [place.to_dict() for place in places_list]
            return jsonify(place_dicts)
    elif place_id:
        place = storage.get(Place, place_id)
        if place:
            return jsonify(place.to_dict())
    raise NotFound()


def delete_specific_place(city_id=None, place_id=None):
    """Deletes a place by its ID."""
    if place_id:
        place = storage.get(Place, place_id)
        if place:
            storage.delete(place)
            storage.save()
            return jsonify({}), 200
    raise NotFound()


def create_new_place(city_id=None, place_id=None):
    """Creates a new place within a specified city."""
    city = storage.get(City, city_id)
    if not city:
        raise NotFound()
    place_data = request.get_json()
    if not isinstance(place_data, dict):
        raise BadRequest(description='Not a JSON')
    if 'user_id' not in place_data or 'name' not in place_data:
        missing = 'user_id' if 'user_id' not in place_data else 'name'
        raise BadRequest(description=f'Missing {missing}')
    user = storage.get(User, place_data['user_id'])
    if not user:
        raise NotFound()
    place_data['city_id'] = city_id
    new_place = Place(**place_data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


def update_existing_place(city_id=None, place_id=None):
    """Updates an existing place's details."""
    excluded_keys = ('id', 'user_id', 'city_id', 'created_at', 'updated_at')
    place = storage.get(Place, place_id)
    if place:
        update_data = request.get_json()
        if not isinstance(update_data, dict):
            raise BadRequest(description='Not a JSON')
        for key, value in update_data.items():
            if key not in excluded_keys:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
    raise NotFound()


@app_views.route('/places_search', methods=['POST'])
def search_for_places():
    """Searches for places based on various criteria."""
    criteria = request.get_json()
    if not isinstance(criteria, dict):
        raise BadRequest(description='Not a JSON')
    all_places = list(storage.all(Place).values())
    search_results = []
    if criteria:
        search_results = filter_places_by_criteria(criteria, all_places)
    else:
        search_results = all_places
    search_results_dicts = [place.to_dict() for place in search_results
                            if 'amenities' not in place.to_dict()]
    return jsonify(search_results_dicts)


def filter_places_by_criteria(criteria, places):
    """Filters places based on state, city, and amenities."""
    filtered_places = []
    if 'states' in criteria:
        for state_id in criteria['states']:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    filtered_places.extend(filter(lambda place:
                                                  place.city_id == city.id,
                                                  places))
    if 'cities' in criteria:
        for city_id in criteria['cities']:
            city = storage.get(City, city_id)
            if city:
                filtered_places.extend(filter(lambda place:
                                              place.city_id == city.id,
                                              places))
    if 'amenities' in criteria:
        filtered_places = filter(lambda place: all(
            amenity.id in [a.id for a in place.amenities]
            for amenity in criteria['amenities']), filtered_places)
    return list(set(filtered_places))
