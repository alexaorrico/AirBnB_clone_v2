#!/usr/bin/python3
"""
Define route for view Place
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models import storage


@app_views.route('/places/<string:place_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def places(place_id=None):
    """Retrieves a Place or All the places"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({})

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')

        for key, value in data.items():
            if key not in ['id', 'user_id', 'city_id',
                           'created_at', 'updated_at']:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict())


@app_views.route('/cities/<string:city_id>/places',
                 strict_slashes=False, methods=['GET', 'POST'])
def place_city(city_id=None):
    """Retrieves a Place or All the places"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        places = [place.to_dict() for place in city.places]
        return jsonify(places)

    if request.method == 'POST':
        data = request.get_json()

        if not data:
            abort(400, 'Not a JSON')
        if 'user_id' not in data:
            abort(400, 'Missing user_id')

        user = storage.get(User, data.get('user_id'))
        if user is None:
            abort(404)
        if 'name' not in data:
            abort(400, 'Missing name')

        data['city_id'] = city_id
        place = Place(**data)
        place.save()
        return jsonify(place.to_dict()), 201


@app_views.route('/places_search', strict_slashes=False, methods=['POST'])
def search_places():
    data = request.get_json()

    if not data:
        abort(400, 'Not a JSON')

    states_id = data.get('states', [])
    cities_id = data.get('cities', [])
    amenities_id = data.get('amenities', [])

    cities = [storage.get(City, city_id) for city_id in cities_id]
    cities = list(filter(None, cities))
    for state_id in states_id:
        state = storage.get(State, state_id)
        if state:
            for city in state.cities:
                if city not in cities:
                    cities.append(city)

    if not cities:
        cities = [city for city in storage.all(City).values()]

    places = [place for city in cities
              for place in city.places]

    filtered_places = []
    for place in places:
        place_amenities_id = [amenity.id for amenity in place.amenities]
        valid = all(amenity_id in place_amenities_id
                    for amenity_id in amenities_id)
        if valid:
            place_dict = place.to_dict()
            del place_dict['amenities']
            filtered_places.append(place_dict)

    return jsonify(filtered_places)
