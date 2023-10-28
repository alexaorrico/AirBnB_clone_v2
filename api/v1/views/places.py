#!/usr/bin/python3
"""Places Views"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.place import Place
from models.city import City
from models.user import User
from flask import abort
from flask import make_response
from flask import request
import json
from os import getenv


@app_views.route('cities/<city_id>/places',
                 methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retuens places according to id of city obj
    or 404 error
    """
    if city_id:
        dic_city = storage.get(City, city_id)
        if dic_city is None:
            abort(404)
        else:
            places = storage.all(Place).values()
            list_places = []
            for place in places:
                if place.city_id == city_id:
                    list_places.append(place.to_dict())
            return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Return place according class and id of the place
    otherwise 404 error
    """
    if place_id:
        dic_place = storage.get(Place, place_id)
        if dic_place is None:
            abort(404)
        else:
            return jsonify(dic_place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes an obj place if it exists
    otherwise return 404 error
    """
    if place_id:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        else:
            storage.delete(place)
            storage.save()
            return make_response(jsonify({}), 200)


@app_views.route('cities/<city_id>/places',
                 methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Create a new place, otherwise raise 404 error if name exists"""
    if city_id:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    reque = request.get_json()

    if "user_id" not in reque:
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    user = storage.get(User, reque['user_id'])
    if user is None:
        abort(404)

    if "name" not in reque:
        return make_response(jsonify({"error": "Missing name"}), 400)
    reque['city_id'] = city_id
    places = Place(**reque)
    places.save()
    return make_response(jsonify(places.to_dict()), 201)


@app_views.route('places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates attributes from a place obj"""
    if place_id:
        places_obj = storage.get(Place, place_id)
        if places_obj is None:
            abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    reque = request.get_json()
    for key, value in reque.items():
        if key not in [
            'id',
            'user_id',
            'city_id',
            'created_at',
                'updated_at']:
            setattr(places_obj, key, value)
    places_obj.save()
    return make_response(jsonify(places_obj.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def places_search():
    """Retrieves all place objs depending of
    json in the request body
    """
    body_reque = request.get_json()
    if body_reque is None:
        abort(400, 'Not a JSON')

    if not body_reque or (
            not body_reque.get('states') and
            not body_reque.get('cities') and
            not body_reque.get('amenities')
    ):
        places = storage.all(Place)
        return jsonify([place.to_dict() for place in places.values()])

    places = []

    if body_reque.get('states'):
        states = [storage.get("State", id) for id in body_reque.get('states')]

        for state in states:
            for city in state.cities:
                for place in city.places:
                    places.append(place)

    if body_reque.get('cities'):
        cities = [storage.get("City", id) for id in body_reque.get('cities')]

        for city in cities:
            for place in city.places:
                if place not in places:
                    places.append(place)

    if not places:
        places = storage.all(Place)
        places = [place for place in places.values()]

    if body_reque.get('amenities'):
        ams = [storage.get("Amenity", id)
               for id in body_reque.get('amenities')]
        m = 0
        limit = len(places)
        HBNB_API_HOST = getenv('HBNB_API_HOST')
        HBNB_API_PORT = getenv('HBNB_API_PORT')

        port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
        first_url = "http://0.0.0.0:{}/api/v1/places/".format(port)
        while m < limit:
            place = places[m]
            url = "{}/amenities".format(first_url, place.id)
            reque = url.format(place.id)
            response = requests.get(reque)
            am_d = json.loads(response.text)
            amenities = [storage.get("Amenity", o['id']) for o in am_d]
            for amenity in ams:
                if amenity not in amenities:
                    places.pop(m)
                    m -= 1
                    limit -= 1
                    break
            m += 1
    return jsonify([place.to_dict() for place in places])
