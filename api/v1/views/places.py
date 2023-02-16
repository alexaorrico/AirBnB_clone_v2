#!/usr/bin/python3

"""places view module"""

from api.v1.views import (app_views)
from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify, abort, request
import models
import os


@app_views.route('/cities/<city_id>/places',
                 methods=["GET"], strict_slashes=False)
def places(city_id):
    """return all the places"""
    cities = models.storage.get(City, city_id)
    if city_id is None:
        return abort(404)
    if cities is None:
        return abort(404)
    return jsonify([place.to_dict() for place in cities.places])


@app_views.route('/places/<place_id>', methods=["GET"], strict_slashes=False)
def get_place_by_id(place_id=None):
    """return a by id or 404"""
    place = models.storage.get(Place, place_id)
    if place_id is None:
        return abort(404)
    if place is None:
        return abort(404)

    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """delete place data by id"""
    place = models.storage.get(Place, place_id)
    if place_id is None:
        return abort(404)
    if place is None:
        return abort(404)

    models.storage.delete(place)
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"], strict_slashes=False)
def add_place(city_id):
    """add new place"""
    try:
        req_data = request.get_json(force=True)
    except Exception:
        req_data = None
    if req_data is None:
        return "Not a JSON", 400
    city = models.storage.get(City, city_id)
    if city is None:
        return abort(404)
    if "user_id" not in req_data.keys():
        return "Missing user_id", 400
    user = models.storage.get(User, req_data.get("user_id"))
    if user is None:
        return abort(404)
    if "name" not in req_data.keys():
        return "Missing name", 400
    req_data["city_id"] = city_id
    new_place = Place(**req_data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """update place object"""
    try:
        req_data = request.get_json(force=True)
    except Exception:
        return "Not a JSON", 400
    place = models.storage.get(Place, place_id)
    if place is None:
        return abort(404)
    for key in ("id", "created_at", "updated_at", "user_id", "city_id"):
        req_data.pop(key, None)
    for k, v in req_data.items():
        setattr(place, k, v)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def list_places():
    """Example endpoint list all places of a JSON body
    Retrieves a list of all places of a JSON body
    ---
    parameters:
      - name: city_id
        in: path
        type: string
        enum: ['None', "1da255c0-f023-4779-8134-2b1b40f87683"]
        required: true
        default: None
    definitions:
      Place:
        type: object
        properties:
          __class__:
            type: string
            description: The string of class object
          created_at:
            type: string
            description: The date the object created
          description:
            type: string
            description: The description of the place
          id:
            type: string
            description: The id of the place
          latitude:
            type: float
          longitude:
            type: float
          max_guest:
            type: int
            description: The maximum guest allowed
          name:
            type: string
            description: name of the place
          number_bathrooms:
            type: int
          number_rooms:
            type: int
          price_by_night:
            type: int
          updated_at:
            type: string
            description: The date the object was updated
          user_id:
            type: string
            description: id of the owner of the place
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      200:
        description: A list of a dictionary of the desire objects
        schema:
          $ref: '#/definitions/Place'
        examples:
            [{"__class__": "Place",
              "created_at": "2017-03-25T02:17:06",
              "id": "dacec983-cec4-4f68-bd7f-af9068a305f5",
              "name": "The Lynn House",
              "city_id": "1721b75c-e0b2-46ae-8dd2-f86b62fb46e6",
              "user_id": "3ea61b06-e22a-459b-bb96-d900fb8f843a",
              "description": "Our place is 2 blocks from Vista Park",
              "number_rooms": 2,
              "number_bathrooms": 2,
              "max_guest": 4,
              "price_by_night": 82,
              "latitude": 31.4141,
              "longitude": -109.879,
              "updated_at": "2017-03-25T02:17:06"
               },
             "..."]
     """
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        return "Not a JSON", 400
    if not r:
        return jsonify([e.to_json() for e in
                        models.storage.all(Place).values()])

    all_cities_id = r.get(City, [])
    states = r.get("states")
    if states:
        all_states = [models.storage.get("State", s) for s in states]
        all_states = [a for a in all_states if a is not None]
        all_cities_id += [c.id for s in all_states for c in s.cities]
    all_cities_id = list(set(all_cities_id))

    all_amenities = r.get("amenities")
    all_places = []
    if all_cities_id or all_amenities:
        all_places2 = models.storage.all(Place).values()
        if all_cities_id:
            all_places2 = [p for p in all_places2 if
                           p.city_id in all_cities_id]
        if all_amenities:
            if os.getenv('HBNB_TYPE_STORAGE', 'fs') != 'db':
                all_places = [p for p in all_places2 if
                              set(all_amenities) <= set(p.amenities_id)]
            else:
                for e in all_places2:
                    flag = True
                    for a in all_amenities:
                        if a not in [i.id for i in e.amenities]:
                            flag = False
                            break
                    if flag:
                        # using amenities make it instance attribute,
                        # not just class check out to_json
                        all_places.append(e)
        else:
            all_places = all_places2
    return jsonify([p.to_json() for p in all_places])
