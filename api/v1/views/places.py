#!/usr/bin/python3
"""creates a new view for Places that handles all Rest Api actions"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models import storage_t
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


def filter_places(places, amenity_ids):
    """Helper function. Takes places amenityID"""
    db_t = storage_t
    if len(amenity_ids) > 0:
        # Get all places with that has amenity in list of amenities
        filtered_place = []
        for place in places:
            place_amenity_ids = place.amenity_ids if db_t != 'db' else []
            if db_t == 'db':
                for amenity in place.amenities:
                    place_amenity_ids.append(amenity.id)
            if len(place_amenity_ids):
                a = set(amenity_ids)
                b = set(place_amenity_ids)
                if a == b or set(a).issubset(set(b)):
                    # compare place amenity ids to request amenity ids
                    c_place = place.to_dict().copy()
                    del c_place['amenities']
                    filtered_place.append(c_place)
        return filtered_place
    else:
        place_list = []
        for place in places:
            place_list.append(place.to_dict())
        return place_list


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
@app_views.route('/places/<place_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def handle_place(city_id=None, place_id=None):
    """Retrieves the list of all place objects by city"""
    if city_id:
        # uses the '/cities/<city_id>/places routes
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        else:
            if request.method == 'GET':
                place_list = []
                for places in city.places:
                    place_list.append(places.to_dict())
                return jsonify(place_list)
            elif request.method == 'POST':
                data = request.get_json()
                if not data:
                    abort(400, 'Not a JSON')
                if not data.get('user_id'):
                    abort(400, 'Missing user_id')
                user_id = storage.get(User, data.get('user_id'))
                if not user_id:
                    abort(404)
                if not data.get('name'):
                    abort(400, 'Missing name')
                data["city_id"] = city_id
                new_obj = Place(**data)
                new_obj.save()
                return jsonify(new_obj.to_dict()), 201

    if place_id:
        # uses the '/places/<place_id>' route
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        else:
            if request.method == 'GET':
                return jsonify(place.to_dict())
            elif request.method == 'DELETE':
                storage.delete(place)
                storage.save()
                return jsonify({}), 200
            elif request.method == 'PUT':
                ignore_keys = ["id", "created_at", "updated_at", "user_id",
                               "city_id"]
                data = request.get_json()
                if not data:
                    abort(400, 'Not a JSON')
                for key, value in data.items():
                    if key in ignore_keys:
                        continue
                    setattr(place, key, value)
                place.save()
                return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Retrieves all ``Place`` objects depending of
       the JSON in the body of the request.
    """
    payload = request.get_json()
    if payload is None:
        abort(400, 'Not a JSON')

    if not payload or len(payload) == 0:  # Check for empty dictionary
        places = storage.all(Place).values()
        place_list = []
        for place in places:
            place_list.append(place.to_dict())
        return jsonify(place_list), 200

    # Get all need lists if available.
    state_ids = payload.get('states') if payload.get('states') else []
    city_ids = payload.get('cities') if payload.get('cities') else []
    amenity_ids = payload.get('amenities') if payload.get('amenities') else []

    if len(state_ids) > 0 or len(city_ids) > 0:
        city_ids_state = []
        if len(state_ids) > 0:
            for state_id in state_ids:
                state = storage.get(State, state_id)
                if not state:
                    abort(404)
                for city in state.cities:
                    city_ids_state.append(city.id)
        city_ids = list(set(city_ids + city_ids_state))
        places = []
        for city_id in city_ids:
            city = storage.get(City, city_id)
            if not city:
                abort(404)
            for place in city.places:
                places.append(place)
        return jsonify(filter_places(places, amenity_ids)), 200
    else:
        places = storage.all(Place).values()
        return jsonify(filter_places(places, amenity_ids)), 200
