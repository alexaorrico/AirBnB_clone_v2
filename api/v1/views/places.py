#!/usr/bin/python3
"""
Create a view for Place objects - handles all default RESTful API actions ...
"""
# Import necessary modules
from flask import jsonify, abort, request

# Import the required models
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models.amenities import Amenity
from models import storage
from api.v1.views import aap_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                    strict_slashes=False)
def get_places_by_cities(city_id):
    """
    Retrieves the list of all Place objects of a City
    """
    city = storage.get(City, city_id)
    if not city:
        return abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                    strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a Place object.
    """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        return abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """
    Retrieves a Place object.
    """
    place = storage.get(Place, place_id)
    if place:
        sorage.delete(place)
        storage.save()
        return jsonify(()), 200
    else:
        return abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'], 
                    strict_slashes=False)
def create_place(city_id):
    """
    Creates a Place object.
    """
    city = storage.get(City, city_id)
    if not city:
        return abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missung user_id')
    if 'name' not in data:
        abort(400, 'Missing name')

    user = storage.get(User, data['user_id'])
    if not user:
        return abort(404)

    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place object.
    """
    place = storage.get(Place, place_id)
    if place:
        if not request.get_json():
            abort(400, 'Not a JSON')

        data = request.get_json()
        ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
    else:
        return abort(404)


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """
    Retrieves Place objects based on the provided JSON search criteria
    """
    if request.content_type != 'application/json':
        return abort(400, "Not a JSON")
    if not request.get_json():
        return abprt(400, "Not a JSON")
    
    data = request.get_json()

    if data:
        states = data.get('states')
        cities = data.get('cities')
        amenities = data.get('amenities')
    if not (states or cities or amenities):
        places = storage.all(Place).values()
        list_places = [place.to_dict() for place in places]
        return jsonify(list_places)
    list_places = []

    if states:
        states_obj = [storage.get(State, state_id) for state_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, city_id) for city_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            all_places = storage.all(Place).values()
            amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
            for place in all_places:
                if all([am in place.amenities for am in amenities_obj]):
                    list_places.append(place)

        place = []
        for plc_obj in list_places:
            plc_dict = plc_obj.to_dict()
            plc_dict.pop('amenities', None)
            places.append(plc_dict)
        return jsonify(places)                  
