#!/usr/bin/python3
"""Place API"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity


@app_views.route("/cities/<string:city_id>/places", strict_slashes=False,
                 methods=['GET'])
def get_city_places(city_id):
    """Returns all places objects in a city"""

    city = storage.get(City, city_id)
    if city is not None:
        places = [place.to_dict() for place in city.places]
        return jsonify(places)
    else:
        return jsonify({'error': 'Not found'}), 404


@app_views.route("/places/<string:place_id>", strict_slashes=False,
                 methods=['GET'])
def get_place(place_id):
    """Returns a place with a given id"""

    place = storage.get(Place, place_id)
    if place is not None:
        return jsonify(place.to_dict())
    else:
        return jsonify({'error': 'Not found'}), 404


@app_views.route("/places/<string:place_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    """Delete a place"""
    place = storage.get(Place, place_id)
    if place is not None:
        place.delete()
        return jsonify({})
    return jsonify({'error': 'Not found'}), 404


@app_views.route("/cities/<string:city_id>/places", strict_slashes=False,
                 methods=['POST'])
def create_place(city_id):
    """Create a place"""

    city = storage.get(City, city_id)
    if city is not None:
        if request.is_json:
            data = request.get_json()
            user_id = data.get('user_id', None)
            place_name = data.get('name', None)
            longitude = data.get('longitude', None)
            latitude = data.get('latitude', None)
            description = data.get('description',  None)
            number_rooms = data.get('number_rooms',  0)
            number_bathrooms = data.get('number_bathrooms',  0)
            max_guest = data.get('max_guest',  0)
            price_by_night = data.get('price_by_night',  0)
            if user_id is None:
                return jsonify({'error': 'Missing user_id'}), 400
            user = storage.get(User, user_id)
            if user is None:
                return jsonify({'error': 'Not found'}), 404
            if place_name is None:
                return jsonify({'error': 'Missing name'}), 400
            place = Place(user_id=user_id,
                          city_id=city_id,
                          name=place_name,
                          number_rooms=number_rooms,
                          number_bathrooms=number_bathrooms,
                          max_guest=max_guest,
                          price_by_night=price_by_night)
            if latitude is not None:
                place.latitude = float(latitude)
            if longitude is not None:
                place.longitude = float(longitude)
            if description is not None:
                place.description = description

            place.save()
            return jsonify(place.to_dict()), 201
        return jsonify({'error': 'Not a JSON'}), 400
    return jsonify({'error': 'Not found'}), 404


@app_views.route("/places/<string:place_id>", strict_slashes=False,
                 methods=['PUT'])
def update_place(place_id):
    """Updates a place"""
    place = storage.get(Place, place_id)
    if place is not None:
        if request.is_json:
            data = request.get_json()
            data = {k: v for k, v in data.items() if k != 'id' and
                    k != 'created_at' and k != 'updated_at' and
                    k != 'user_id' and k != 'city_id'}
            for k, v in data.items():
                setattr(place, k, v)
            place.save()
            return jsonify(place.to_dict()), 200
        return jsonify({'error': 'Not a JSON'}), 400
    return jsonify({'error': 'Not found'}), 404


@app_views.route("/places_search", strict_slashes=False,
                 methods=['POST'])
def places_search():
    """Retrieves all Place objects depending of the JSON
    in the body of the request"""

    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    states = data.get("states", [])
    cities = data.get("cities", [])
    amenities = data.get("amenities", [])
    places = []
    if len(states) == 0 and len(cities) == 0 and\
       len(amenities) == 0:
        places = list(storage.all(Place).values())

    if len(states) > 0:
        for id in states:
            state = storage.get(State, id)
            if state is not None:
                for city in state.cities:
                    places.extend(city.places)
                    if city.id in cities:
                        cities.remove(city.id)

    if len(cities) > 0:
        for id in cities:
            city = storage.get(City, id)
            if city is not None:
                places.extend(city.places)

    if len(amenities) > 0:
        for place in places:
            if len(amenities) != len(place.amenities):
                places.remove(place)
                continue
            for amenity in place.amenities:
                if amenity.id not in amenities:
                    places.remove(place)
                    break

    places = [place.to_dict() for place in places]
    return jsonify(places)
