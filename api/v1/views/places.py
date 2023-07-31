#!/usr/bin/python3
"""
A new view for Place objects that handles all default RESTFul API actions
"""
from flask import abort
from flask import jsonify
from flask import request

from . import User
from . import City
from . import Place
from . import State
from . import Amenity
from . import storage
from . import app_views

# f are class properties to validate the request payload
f = ("user_id", "name", "description", "number_rooms", "number_bathrooms",
     "max_guest", "price_by_night", "latitude", "longitude")


def validate_payload(payload={}):
    """
    validate type field inputs, ensures the right types are given
    """
    for _ in f[3:7]:
        value = payload.get(_, None)
        if value is not None:
            try:
                payload.update({_: int(value)})
            except Exception:
                del payload[_]
    for _ in f[-2:]:
        value = payload.get(_, None)
        if value is not None:
            try:
                payload.update({_: float(value)})
            except Exception:
                del payload[_]
    return payload


@app_views.route("/cities/<city_id>/places",
                 methods=["GET", "POST"], strict_slashes=False)
def places_by_city(city_id):
    """
    Creates a new Place object
    Retrieves the list of all Place objects of a State
    Args:
        city_id: primary key of an existing Place object
    """
    city = storage.get(City, str(city_id))
    if city is None:
        abort(404, description="Not found")
    if request.method == "GET":
        places = {k: v
                  for k, v in storage.all(Place).items()
                  if v.city_id == city_id}
        return jsonify([p.to_dict() for p in places.values()])
    else:
        body = request.get_json(silent=True)
        if request.is_json and body is not None:
            pay = {k: str(v) for k, v in body.items() if k in f}
            for k in f[0:2]:
                if not pay.get(k, None):
                    abort(400, description="Missing " + k)
                if k == "user_id" and\
                        not storage.get(User, str(pay.get("user_id"))):
                    abort(404, description="Not found")
            pay.update({"city_id": city_id})
            new_place = Place(**(validate_payload(pay)))
            storage.new(new_place), storage.save()
            return jsonify(new_place.to_dict()), 201
        abort(400, description="Not a JSON")


@app_views.route("/places/<place_id>",
                 methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def one_place(place_id):
    """
    Deletes an existing City object
    Retrieves an existing City object
    Updates an existing City object
    Args:
        city_id: primary key of an existing city object
    """
    place = storage.get(Place, str(place_id))
    if not place:
        abort(404, description="Not found")
    if request.method == "GET":
        return jsonify(place.to_dict())
    elif request.method == "DELETE":
        storage.delete(place), storage.save()
        return jsonify({})
    else:
        body = request.get_json(silent=True)
        if request.is_json and body is not None:
            pay = validate_payload(body)
            [setattr(place, k, str(v)) for k, v in pay.items() if k in f[1:]]
            place.save()
            return jsonify(place.to_dict()), 200
        abort(400, description="Not a JSON")


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def places_search():
    """
    Search for places by states and cities inclusive, filter by amenities
    """
    body = request.get_json(silent=True)
    if body is not None:
        if body == {} or all([v == [] for k, v in body.items()]):
            places = storage.all(Place)
            li_places = [v.to_dict() for k, v in places.items()]
            return jsonify(li_places), 200
        pslist = []
        if 'states' in body and body['states'] != []:
            for state_id in body['states']:
                state = storage.get(State, state_id)
                for city in state.cities:
                    pslist.extend(city.places)
        if 'cities' in body and body['cities'] != []:
            for city_id in body['cities']:
                city = storage.get(City, city_id)
                for place in city.places:
                    if place not in pslist:
                        pslist.append(place)
        if pslist == []:
            places = storage.all(Place)
            pslist = [v for k, v in places.items()]
        li_places = [place.to_dict() for place in pslist]
        if 'amenities' in body and body['amenities'] != []:
            amenitylist = [storage.get(Amenity, amenity_id)
                           for amenity_id in body['amenities']]
            for place in pslist:
                if all(amenity in place.amenities
                       for amenity in amenitylist) is False:
                    for li_place in li_places:
                        if place.id == li_place['id']:
                            li_places.remove(li_place)
        return jsonify(li_places), 200
    else:
        abort(400, {'message': 'Not a JSON'})
