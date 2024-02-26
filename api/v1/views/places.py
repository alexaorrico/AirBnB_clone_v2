#!/usr/bin/python3
""" Module handling default RESTful API actions for Places """
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/place/get_places.yml', methods=['GET'])
def get_places_by_city(city_id):
    """
    Retrieve the list of all Place objects for a given City
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    places = [place.to_dict() for place in city.places]

    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/place/get_place.yml', methods=['GET'])
def get_single_place(place_id):
    """
    Retrieve a specific Place object
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/place/delete_place.yml', methods=['DELETE'])
def delete_single_place(place_id):
    """
    Delete a specific Place object
    """

    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/place/post_place.yml', methods=['POST'])
def create_place_in_city(city_id):
    """
    Create a new Place in a City
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    user_id = data.get('user_id')
    if not user_id:
        abort(400, description="Missing user_id")

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    name = data.get('name')
    if not name:
        abort(400, description="Missing name")

    data["city_id"] = city_id
    new_place = Place(**data)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/place/put_place.yml', methods=['PUT'])
def update_single_place(place_id):
    """
    Update a specific Place object
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
@swag_from('documentation/place/post_search.yml', methods=['POST'])
def search_places():
    """
    Retrieve Place objects based on the JSON in the request body
    """
    if request.get_json() is None:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if not data or not any(data.values()):
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    filtered_places = set()

    if states:
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                filtered_places.update(state.cities)

    if cities:
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                filtered_places.add(city)

    if amenities:
        amenities_set = set(storage.get(Amenity, amenity_id) for amenity_id in amenities)
        filtered_places = [place for place in filtered_places if amenities_set.issubset(set(place.amenities))]

    result_places = []
    for place in filtered_places:
        result_places.extend(place.places)

    result = [place.to_dict() for place in result_places]
    return jsonify(result)

