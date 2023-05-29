#!/usr/bin/python3
"""HTTP methods for RESTFul API"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place


@app_views.route('/cities/<city_id>/places')
def all_place(city_id=None):
    """GET places within cities"""
    list_places = []
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    else:
        all_places = storage.all("Place").values()
        for place in all_places:
            if place.city_id == str(city_id):
                list_places.append(place.to_dict())
        return jsonify(list_places)


@app_views.route('/places/<place_id>')
def get_places(place_id=None):
    """GET place method"""
    places = storage.get("Place", place_id)
    if places is None:
        abort(404)
    else:
        return jsonify(places.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE', 'PUT'])
def place_methods(place_id=None):
    """'DELETE' methods"""
    obj_place = storage.get("Place", place_id)
    if obj_place is None:
        abort(404)
    if request.method == 'DELETE':
        obj_place.delete()
        storage.save()
        return (jsonify({}), 200)
    if request.method == 'PUT':
        if not request.is_json:
            abort(400, "Not a JSON")
        do_put = request.get_json()
        for k, v in do_put.items():
            if(k is not "id" and k is not "created_at" and
               k is not "updated_at" and
               k is not "user_id" and k is not "city_id"):
                setattr(obj_place, k, v)
        obj_place.save()
        return (jsonify(obj_place.to_dict()), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def place_post(city_id):
    """POST method"""
    city_objs = storage.get("City", city_id)
    if city_objs is None:
        abort(404)
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request.json:
        return jsonify({"error": "Missing user_id"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    do_post = request.get_json()
    new_usr = do_post.get("user_id")
    usr = storage.get("User", new_usr)
    if usr is None:
        abort(404)
    new_place = Place(**do_post)
    setattr(new_place, "city_id", city_id)
    new_place.save()
    return (jsonify(new_place.to_dict()), 201)

@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Searches for Place objects based on the JSON request body"""
    try:
        search_params = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')

    states = search_params.get('states')
    cities = search_params.get('cities')
    amenities = search_params.get('amenities')

    places = storage.all(Place).values()

    if not states and not cities and not amenities:
        return jsonify([place.to_dict() for place in places])

    if states:
        state_places = []
        for state_id in states:
            state = storage.get("State", state_id)
            if state:
                state_places.extend(state.places)
        places = [place for place in places if place in state_places]

    if cities:
        city_places = []
        for city_id in cities:
            city = storage.get("City", city_id)
            if city:
                city_places.extend(city.places)
        places = [place for place in places if place in city_places]

    if amenities:
        amenity_places = []
        for amenity_id in amenities:
            amenity = storage.get("Amenity", amenity_id)
            if amenity:
                amenity_places.extend(amenity.places)
        places = [place for place in places if all(amenity in place.amenities for amenity in amenity_places)]

    return jsonify([place.to_dict() for place in places])
