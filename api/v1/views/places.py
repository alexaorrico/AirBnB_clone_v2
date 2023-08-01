#!/usr/bin/python3
"""
module state.py
"""

from flask import abort, jsonify, request
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def placesObjOfCity(city_id):
    """Retrieves the list of all place objects of a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    placeList = []
    """same as cities_list = [city.to_dict() for city in state.cities]"""
    for place in city.places:
        placeList.append(place.to_dict())
    return jsonify(placeList)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def placeObj(place_id):
    """Retrieves a Place object."""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def placeDeleteWithId(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def createPlace(city_id):
    """Creates a Place: POST /api/v1//cities/<city_id>/places"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    city = storage.get(City, city_id)
    if city:
        newPlaceData = request.get_json()
        if not newPlaceData.get('name'):
            abort(400, description='Missing name')

        if not newPlaceData.get('user_id'):
            abort(400, description='Missing user_id')

        place_userId = newPlaceData.get('user_id')
        user = storage.get(User, place_userId)
        if not user:
            abort(404)
        newPlaceData['city_id'] = city_id

        newPlaceObj = Place(**newPlaceData)
        storage.new(newPlaceObj)
        storage.save()

        return jsonify(newPlaceObj.to_dict()), 201
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def updatePlace(place_id):
    """Updates a Place object"""
    placeObj = storage.get(Place, place_id)
    if placeObj:
        update = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        ignoredKeys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for k, v in update.items():
            if k not in ignoredKeys:
                setattr(placeObj, k, v)

        storage.save()
        return jsonify(placeObj.to_dict()), 200
    else:
        abort(404)


@app_views.route('/places_search', methods=['POST'])
def places_search():
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    states_list = data.get('states', [])
    cities_list = data.get('cities', [])
    amenities_list = data.get('amenities', [])

    places = set()
    if not states_list and not cities_list:
        places = storage.all(Place).values()
    else:
        states_places = set()
        cities_places = set()

        for state_id in states_list:
            state = storage.get(State, state_id)
            if state:
                states_places.update(state.cities)

        for city_id in cities_list:
            city = storage.get(City, city_id)
            if city:
                cities_places.add(city)

        places.update(states_places)
        places.update(cities_places)

    if amenities_list:
        amenities_set = set([storage.get(Amenity, amenity_id)
                            for amenity_id in amenities_list])
        places = set(filter(lambda place: amenities_set.issubset
                            (set(place.amenities)), places))

    return jsonify([place.to_dict() for place in places])
