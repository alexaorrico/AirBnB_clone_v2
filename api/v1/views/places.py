#!/usr/bin/python3
"""
This is module places
"""
from api.v1.views import (app_views, Place, storage)
from flask import (abort, jsonify, make_response, request)
import os


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def view_places_in_city(city_id):
    """Example endpoint returns a list of all places in a city
    Retrieves all places within a city
    ---
    parameters:
      - name: city_id
        in: path
        type: string
        enum: ['None', '1da255c0-f023-4779-8134-2b1b40f87683']
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
        description: A list of dictionaries of place object
        schema:
          $ref: '#/definitions/Place'
        examples:
            [{
             "__class__": "Place",
             "city_id": "1da255c0-f023-4779-8134-2b1b40f87683",
             "created_at": "2017-03-25T02:17:06",
             "description": "The guest house is located uptown",
             "id": "279b355e-ff9a-4b85-8114-6db7ad2a4cd2",
             "latitude": 29.9493,
             "longitude": -90.1171,
             "max_guest": 2,
             "name": "Guest House by Tulane",
             "number_bathrooms": 1,
             "number_rooms": 0,
             "price_by_night": 60,
             "updated_at": "2017-03-25T02:17:06",
             "user_id": "8394fd35-8a8a-479f-a398-48f53b4a6554"
             }]
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    result = [place.to_json() for place in city.places]
    return jsonify(result)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def view_place(place_id=None):
    """Example endpoint returns a single place
    Retrieves one place with the given id
    ---
    parameters:
      - name: place_id
        in: path
        type: string
        enum: ['None', 279b355e-ff9a-4b85-8114-6db7ad2a4cd2"]
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
        description: A list of a dictionary of a place obj
        schema:
          $ref: '#/definitions/Place'
        examples:
            [{
             "__class__": "Place",
             "city_id": "1da255c0-f023-4779-8134-2b1b40f87683",
             "created_at": "2017-03-25T02:17:06",
             "description": "The guest house is located uptown",
             "id": "279b355e-ff9a-4b85-8114-6db7ad2a4cd2",
             "latitude": 29.9493,
             "longitude": -90.1171,
             "max_guest": 2,
             "name": "Guest House by Tulane",
             "number_bathrooms": 1,
             "number_rooms": 0,
             "price_by_night": 60,
             "updated_at": "2017-03-25T02:17:06",
             "user_id": "8394fd35-8a8a-479f-a398-48f53b4a6554"
             }]
    """
    s = storage.get("Place", place_id)
    if s is None:
        abort(404)
    return jsonify(s.to_json())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id=None):
    """Example endpoint deleting one place
    Deletes a place based on the place_id of the JSON body
    ---
    definitions:
      Place:
        type: object
      Color:
        type: string
      items:
        $ref: '#/definitions/Color'

    responses:
      200:
        description: An empty dictionary
        schema:
          $ref: '#/definitions/City'
        examples:
            {}
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Example endpoint creates a single place
    Create a single place based on the JSON body
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
      201:
        description: A list of a dictionary of a place obj
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
               }]
     """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        return "Not a JSON", 400
    if 'user_id' not in r.keys():
        return "Missing user_id", 400
    user = storage.get("User", r.get("user_id"))
    if user is None:
        abort(404)
    if 'name' not in r.keys():
        return "Missing name", 400
    r["city_id"] = city_id
    s = Place(**r)
    s.save()
    return jsonify(s.to_json()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id=None):
    """Example endpoint creates a single place
    Updates a place based on the JSON body
    ---
    parameters:
      - name: place_id
        in: path
        type: string
        enum: ['None', "279b355e-ff9a-4b85-8114-6db7ad2a4cd2"]
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
        description: A list of a dictionary of a place obj
        schema:
          $ref: '#/definitions/Place'
        examples:
            [{
             "__class__": "Place",
             "city_id": "1da255c0-f023-4779-8134-2b1b40f87683",
             "created_at": "2017-03-25T02:17:06",
             "description": "The guest house is located uptown",
             "id": "279b355e-ff9a-4b85-8114-6db7ad2a4cd2",
             "latitude": 29.9493,
             "longitude": -90.1171,
             "max_guest": 2,
             "name": "Guest House by Tulane",
             "number_bathrooms": 1,
             "number_rooms": 0,
             "price_by_night": 60,
             "updated_at": "2017-03-25T02:17:06",
             "user_id": "8394fd35-8a8a-479f-a398-48f53b4a6554"
             }]
    """
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        return "Not a JSON", 400
    a = storage.get("Place", place_id)
    if a is None:
        abort(404)
    for k in ("id", "user_id", "city_id", "created_at", "updated_at"):
        r.pop(k, None)
    for k, v in r.items():
        setattr(a, k, v)
    a.save()
    return jsonify(a.to_json()), 200


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
        return jsonify([e.to_json() for e in storage.all("Place").values()])

    all_cities_id = r.get("cities", [])
    states = r.get("states")
    if states:
        all_states = [storage.get("State", s) for s in states]
        all_states = [a for a in all_states if a is not None]
        all_cities_id += [c.id for s in all_states for c in s.cities]
    all_cities_id = list(set(all_cities_id))

    all_amenities = r.get("amenities")
    all_places = []
    if all_cities_id or all_amenities:
        all_places2 = storage.all("Place").values()
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
# what to do for junk states, cities, amenities
