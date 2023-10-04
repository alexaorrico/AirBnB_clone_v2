#!/usr/bin/python3
""" Places """
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views, storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'],
                 strict_slashes=False)
def list_places(city_id):
    """List all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places_list = [place.to_dict() for place in city.places]
    return jsonify(places_list)


@app_views.route('/places/<place_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object by place_id"""
    place = storage.get(Place, place_id)
    if place is not None:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object by place_id"""
    place = storage.get(Place, place_id)
    if place is not None:
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place object in a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    request_dict = request.get_json(silent=True)
    if request_dict is not None:
        if 'user_id' not in request_dict or request_dict['user_id'] is None:
            return make_response(jsonify({'error': 'Missing user_id'}), 400)
        user = storage.get(User, request_dict['user_id'])
        if user is None:
            abort(404)
        if 'name' not in request_dict.keys() or request_dict['name'] is None:
            return make_response(jsonify({'error': 'Missing name'}), 400)
        new_place = Place(**request_dict)
        new_place.city_id = city_id
        new_place.save()
        return make_response(jsonify(new_place.to_dict()), 201)
    return make_response(jsonify({"error": "Not a JSON"}), 400)


@app_views.route('/places/<place_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a Place object by place_id"""
    request_dict = request.get_json(silent=True)
    data = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    if request_dict is not None:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        for key, val in request_dict.items():
            if key not in data:
                setattr(place, key, val)
        storage.save()
        return make_response(jsonify(place.to_dict()), 200)
    return make_response(jsonify({"error": "Not a JSON"}), 400)


@app_views.route("/places_search",
                 methods=["POST"],
                 strict_slashes=False)
def places_search():
    """Search for places based on JSON request data."""
    try:
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")

        states = data.get("states", [])
        cities = data.get("cities", [])
        amenities = data.get("amenities", [])

        places = []

        if not states and not cities and not amenities:
            places = storage.all(Place).values()
        else:
            if states:
                states_places = []
                for state_id in states:
                    state = storage.get(State, state_id)
                    if state:
                        states_places.extend(state.cities)
                for city in states_places:
                    if city.id not in cities:
                        cities.append(city.id)

            for city_id in cities:
                city = storage.get(City, city_id)
                if city:
                    places.extend(city.places)

            if amenities:
                amenities_set = set(amenities)
                places = [place for place in places
                          if all(amenity.id in amenities_set
                                 for amenity in place.amenities)]

        result = [place.to_dict() for place in places]
        return jsonify(result)

    except Exception as e:
        abort(400, "Not a JSON")
