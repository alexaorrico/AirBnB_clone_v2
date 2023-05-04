#!/usr/bin/python3
"""Creates a new view for Place objects that handles
all default RESTFul API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_of_city(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    user = storage.get(User, request.get_json().get('user_id'))
    if not user:
        abort(404)
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    data = request.get_json()
    data['city_id'] = city_id
    place = Place(**data)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'])
def search_places():
    """Retrieves all Place objects depending of the JSON in the body
    of the request
    """
    if not request.get_json():
        abort(400, 'Not a JSON')
    json_data = request.get_json()
    states = json_data.get('states', [])
    cities = json_data.get('cities', [])
    amenities = json_data.get('amenities', [])
    if not states and not cities and not amenities:
        places = storage.all('Place').values()
        return jsonify([place.to_dict() for place in places])
    state_objs = [storage.get('State', state_id) for state_id in states]
    city_objs = [storage.get('City', city_id) for city_id in cities]
    places = []
    for state_obj in state_objs:
        if state_obj:
            for city_obj in state_obj.cities:
                if city_obj not in city_objs:
                    city_objs.append(city_obj)
    for city_obj in city_objs:
        if city_obj:
            for place_obj in city_obj.places:
                if all(amenity_id in place_obj.amenities
                       for amenity_id in amenities):
                    places.append(place_obj)
    return jsonify([place.to_dict() for place in places])
