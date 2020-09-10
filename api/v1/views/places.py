#!/usr/bin/python3
""" amenities view class """
from models import storage
from api.v1.views import app_views
from models.state import State
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from flask import jsonify, request, abort, make_response


@app_views.route("/cities/<string:city_id>/places",
                 strict_slashes=False, methods=["GET", "POST"])
def get_place_fromcity(city_id=None):
    """ retrives all places from a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == "GET":
        return jsonify([place.to_dict() for place in city.places])
    if request.method == "POST":
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if request.get_json().get("user_id") is None:
            return make_response(jsonify({'error': 'Missing user_id'}), 400)
        if request.get_json().get("name") is None:
            return make_response(jsonify({'error': 'Missing name'}), 400)
        user = storage.get(User, request.get_json().get("user_id"))
        if user is None:
            abort(404)
        dic = request.get_json()
        dic.update({"city_id": city_id})
        place = Place(**dic)
        place.save()
        return make_response(jsonify(place.to_dict()), 201)


@app_views.route("/places/<string:place_id>",
                 strict_slashes=False, methods=["GET", "DELETE", "PUT"])
def get_place_id(place_id=None):
    """ gets place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == "GET":
        return jsonify(place.to_dict())
    if request.method == "DELETE":
        place.delete()
        storage.save()
        return jsonify({})
    if request.method == "PUT":
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for key, val in request.get_json().items():
            if key not in ['id', 'created_at',
                           'updated_at', 'user_id', 'city_id']:
                setattr(place, key, val)
        place.save()
        return jsonify(place.to_dict())


@app_views.route("/places_search", strict_slashes=False, methods=["POST"])
def places_search():
    """ retrieves all Place objects depending of the JSON
        in the body of the request
    """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    if request.get_json().get("states") is not None:
        if request.get_json().get("cities") is not None:
            place_list = []
            for city_id in request.get_json().get("cities"):
                city = storage.get(City, city_id)
                place_list.append([place.to_dict() for place in city.places])
            return jsonify(place_list)
        else:
            place_list = []
            for state_id in request.get_json().get("states"):
                state = storage.get(State, state_id)
                cities = [city for city in state.cities]
                for city in cities:
                    place_list.append([place.to_dict()
                                      for place in city.places])
            return jsonify(place_list)

    if request.get_json().get("cities") is not None:
            place_list = []
            for city_id in request.get_json().get("cities"):
                city = storage.get(City, city_id)
                place_list.append([place.to_dict() for place in city.places])
            return jsonify(place_list)

    if request.get_json().get("amenities") is not None:
        places = storage.all(Place)
        place_list = []
        for place in places.values():
            for amenity_id in request.get_json().get("amenities"):
                amenity = storage.get(Amenity, amenity_id)
                if amenity in place.amenities:
                    new_dict = place.__dict__.copy()
                    if "amenities" in new_dict:
                        del new_dict["amenities"]
                    if "_sa_instance_state" in new_dict:
                        del new_dict["_sa_instance_state"]
                    if "__class__" not in new_dict:
                        new_dict.update({"__class__": "Place"})
                    place_list.append(new_dict)
        return jsonify(place_list)

    return jsonify([obj.to_dict() for obj in storage.all(Place).values()])
