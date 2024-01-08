#!/usr/bin/python3
"""
contains endpoints(routes) for place objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<string:city_id>/places", strict_slashes=False)
def get_places(city_id):
    """
    Retrieves the list of all Place objects of a City
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [obj.to_dict() for obj in city.places]
    return jsonify(places)


@app_views.route("/places/<string:place_id>", strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a Place object
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<string:place_id>", strict_slashes=False,
                 methods=['DELETE'])
def del_place(place_id):
    """
    Deletes a Place object
    """
    place = storage.get(Place, place_id)
    if place:
        place.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/cities/<string:city_id>/places", strict_slashes=False,
                 methods=['POST'])
def create_place(city_id):
    """
    Creates a Place instance
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    valid_json = request.get_json()

    if valid_json is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in valid_json:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'name' not in valid_json:
        return make_response(jsonify({"error": "Missing name"}), 400)

    valid_json['city_id'] = city_id
    user = storage.get(User, valid_json['user_id'])
    if not user:
        abort(404)
    obj = Place(**valid_json)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route("/places/<string:place_id>", strict_slashes=False,
                 methods=['PUT'])
def update_place(place_id):
    """
    Updates a Place object
    """
    place = storage.get(Place, place_id)
    valid_json = request.get_json()

    if not place:
        abort(404)

    if valid_json is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in valid_json.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def post_places_search():
    """
    retrieves Place objects depending of the JSON in the body of the request.
    """
    valid_json = request.get_json()

    if valid_json:
        states = valid_json.get('states', [])
        cities = valid_json.get('cities', [])
        amenities = valid_json.get('amenities', [])
        amenity_obj = []
        for amenity_id in amenities:
            amenity = storage.get('Amenity', amenity_id)
            if amenity:
                amenity_obj.append(amenity)
        if states == cities == []:
            places = storage.all('Place').values()
        else:
            places = []
            for state_id in states:
                state = storage.get('State', state_id)
                state_cities = state.cities
                for city in state_cities:
                    if city.id not in cities:
                        cities.append(city.id)
            for city_id in cities:
                city = storage.get('City', city_id)
                for place in city.places:
                    places.append(place)
        confirmed_places = []
        for place in places:
            place_amenities = place.amenities
            confirmed_places.append(place.to_dict())
            for amenity in amenity_objects:
                if amenity not in place_amenities:
                    confirmed_places.pop()
                    break
        return jsonify(confirmed_places)
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
