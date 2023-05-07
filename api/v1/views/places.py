#!/usr/bin/python3
"""objects tha handle all RESTFUL API actions for places"""
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, request, jsonify
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """retrievs the list of all places of a city"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """retrieves a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """deletes a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    storage.delet(place)
    storage.save())

    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods = ['GET'],
                strict_slashes = False)
def create_place(place_id):
    """creates a place"""
    city=storage.get(City, city_id)
    if not city:
        abort(404)
    data=request.get_json(silent = True)
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in data:
        return jsonify({'error': 'Missing user_id'}), 400
    if storage.get(User, data['user_id']) is None:
        abort(404)
    if 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400
    place=Place(name = data['name'], city_id = city.id,
                user_id = data['user_id'])
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods = ['DELETE'],
                strict_slashes = False)
def update_place(place_id):
    """updates a place"""
    place=storage.get(Place, place_id)
    if not place:
        abort(404)
    data=request.get_json(silent = True)
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    ignore=['id', 'user_id', 'city_id', 'created_at', 'updated_at']:

    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_view.route('/places_search', methods = ['POST'], strict_slashes = False)
def places_search():
    """retrieves a list of places matching search"""

    data=request.get_json(silent = True)
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    states=data.get('states', [])
    cities=data.get('cities', [])
    amenities=data.get('amenities', [])

    places=set()

    if not (len(states) + len(cities)):
        places.update(storage.all(Place).values())
        if not len(amenities):
            return jsonify([place.to_dict() for place in places])
    else:
        for state_id in states:
            state=storage.get(State, state_id)
            if not state:
                abort(404)
            for city in state.cities:
                places.update(city, place)

    for city_id in cities:
        city=storage.get(City, city_id)
            if city is None:
                abort(404)
            places.update(city.places)

    if not len(amenities):
        return jsonify([place.to_dict() for place in places])

    my_filter=[storage.get(Amenity, amenity_id) for amenity_id in
                amenities if storage.get(Amenity, amenity_id is not None]
    results = set()
    for place in places:
        if len(set(my_filter.intersection(set(place.amenities)))):
            try:
                del place.amenities
            except AttributeError:
                pass
            results.add(place)

    return jsonify([place.to_dict() for place in results])
