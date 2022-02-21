#!/usr/bin/python3
"""
This is module places
"""
from api.v1.views import (
    app_views,
    storage
)
from flask import (
    abort,
    jsonify,
    make_response,
    request
)
from models.city import City
from models.place import Place

# this helps incase you use a .env file
try:
    from decouple import config as getenv
except ImportError:
    from os import getenv

@app_views.route('/cities/<city_id>/places', methods=['GET'])
def view_places_in_city(city_id):
    """
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

    responses:
      200:
        description: A list of dictionaries of place object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    result = [place.to_dict() for place in city.places]
    return jsonify(result)


@app_views.route('/places/<place_id>', methods=['GET'])
def view_place(place_id=None):
    """
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

    responses:
      200:
        description: A list of a dictionary of a place obj

    """
    s = storage.get(Place, place_id)
    if s is None:
        abort(404)
    return jsonify(s.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id=None):
    """Example endpoint deleting one place
    Deletes a place based on the place_id of the JSON body
    ---
    definitions:
      Place:
        type: object

    responses:
      200:
        description: An empty dictionary
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """
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

    responses:
      201:
        description: A list of a dictionary of a place obj
     """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    try:
        r = request.get_json()
    except Exception:
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
    return jsonify(s.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id=None):
    """
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

    responses:
      200:
        description: A list of a dictionary of a place obj

    """
    try:
        r = request.get_json()
    except Exception:
        r = None
    if r is None:
        return "Not a JSON", 400
    a = storage.get(Place, place_id)
    if a is None:
        abort(404)
    for k in ("id", "user_id", "city_id", "created_at", "updated_at"):
        r.pop(k, None)
    for k, v in r.items():
        setattr(a, k, v)
    a.save()
    return jsonify(a.to_dict()), 200


@app_views.route('/places_search', methods=['POST'])
def list_places():
    """
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
    responses:
      200:
        description: A list of a dictionary of the desire objects
     """
    try:
        r = request.get_json()
    except Exception:
        r = None
    if r is None:
        return "Not a JSON", 400
    if not r:
        return jsonify([e.to_dict() for e in storage.all(Place).values()])

    all_cities_id = r.get("cities", None)
    states = r.get("states", None)
    if states:
        all_states = [storage.get("State", s) for s in states]
        all_states = [a for a in all_states if a is not None]
        if all_cities_id:
            all_cities_id += [c.id for s in all_states for c in s.cities]
        else:
            all_cities_id = [c.id for s in all_states for c in s.cities]
    if all_cities_id:
        all_cities_id = list(set(all_cities_id))

    all_amenities = r.get("amenities")
    all_places = []
    if all_cities_id or all_amenities:
        all_places2 = storage.all("Place").values()
        if all_cities_id:
            all_places2 = [p for p in all_places2 if
                           p.city_id in all_cities_id]
        if all_amenities:
            if getenv('HBNB_TYPE_STORAGE', 'fs') != 'db':
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
                        # not just class check out to_dict
                        all_places.append(e)
        else:
            all_places = all_places2
    return jsonify([p.to_dict() for p in all_places])
# what to do for junk states, cities, amenities
