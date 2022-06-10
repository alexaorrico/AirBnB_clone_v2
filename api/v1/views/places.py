#!/usr/bin/python3
""" Place view """
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route('cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def list_places(city_id):
    """
    Retrieves the list of all Place objects of a City
    ---
    tags:
      - Place
    parameters:
      - name: city_id
        in: path
        required: true
    responses:
      200:
        description: All places from a given city
        schema:
          type: array
          items:
            type: object
            properties:
              __class__:
                type: string
              city_id:
                type: string
              created_at:
                type: string
              description:
                type: string
              id:
                type: string
              latitude:
                type: number
              longitude:
                type: number
              max_guest:
                type: number
              name:
                type: string
              number_bathrooms:
                type: number
              number_rooms:
                type: number
              updated_at:
                type: string
              user_id:
                type: string
          example:
            [
              {
                "__class__": "Place",
                "city_id": "f1414b88-190d-4518-866a-01634d15c8af",
                "created_at": "2022-05-31T20:42:53.350872",
                "description": ,
                "id": "f1414b88-190d-4518-866a-01634d15c8af",
                "latitude": 29.9493,
                "longitude": -90.1171,
                "max_guest": 2,
                "name": "House 1",
                "number_bathrooms": 1,
                "number_rooms": 1,
                "price_by_night": 60,
                "updated_at": "2022-05-31T20:42:53.350872",
                "user_id": "9d475737-0548-4f49-a404-7b347d1f01de"
              },
              {
                "__class__": "Place",
                "city_id": "20ca9e29-a7cf-4b5f-a2e9-714e48b765a2",
                "created_at": "2022-05-31T20:42:53.350872",
                "description": ,
                "id": "a6f8cc34-14da-4624-b7b2-7abcca47390b",
                "latitude": 29.9666,
                "longitude": -90.0519,
                "max_guest": 1,
                "name": "House 2",
                "number_bathrooms": 1,
                "number_rooms": 1,
                "price_by_night": 40,
                "updated_at": "2022-05-31T20:42:53.350872",
                "user_id": "9d475737-0548-4f49-a404-7b347d1f01de"
              }
            ]
      404:
        description: No city found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not found"
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place(place_id):
    """
    Retrieves a Place object
    ---
    tags:
      - Place
    parameters:
      - name: place_id
        in: path
        required: true
    responses:
      404:
        description: No place found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not found"
      200:
        description: Place found
        schema:
          type: object
          properties:
            __class__:
              type: string
            city_id:
              type: string
            created_at:
              type: string
            description:
              type: string
            id:
              type: string
            latitude:
              type: number
            longitude:
              type: number
            max_guest:
              type: number
            name:
              type: string
            number_bathrooms:
              type: number
            number_rooms:
              type: number
            updated_at:
              type: string
            user_id:
              type: string
          example:
            __class__: "Place"
            city_id: "0f7e8c95-d238-42b3-aa27-a7bc7c06cf5d"
            created_at: "2022-05-31T20:42:53.350872"
            description: "The best option, you can walk through the beautiful
            gardens, it has air conditioning and a bathtub to take a nice
            bath as you like."
            id: "e311439a-c4ab-451a-848b-3db2648090df"
            latitude: 37.774
            longitude: -122.431
            max_guest: 6
            name: "Lovely Place"
            number_bathrooms: 3
            number_rooms: 1
            price_by_night: 120
            updated_at: "2022-05-31T20:42:53.350872"
            user_id: "031f949b-750e-49d0-b088-602abeebc47c"
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def place_delete(place_id):
    """
    Deletes a Place object
    ---
    tags:
      - Place
    parameters:
      - name: place_id
        in: path
        required: true
    responses:
      200:
        description: Place deleted
        schema:
          type: object
      404:
        description: No place found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not found"
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def new_place(city_id):
    """
    Creates a new Place
    ---
    tags:
      - Place
    parameters:
      - name: create_place
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - user_id
          properties:
            name:
              type: string
            user_id:
              type: string
          example:
            name: "Lovely Place"
            user_id: "031f949b-750e-49d0-b088-602abeebc47c"
    responses:
      201:
        description: Place created
        schema:
          type: object
          properties:
            __class__:
              type: string
            city_id:
              type: string
            created_at:
              type: string
            description:
              type: string
            id:
              type: string
            latitude:
              type: number
            longitude:
              type: number
            max_guest:
              type: number
            name:
              type: string
            number_bathrooms:
              type: number
            number_rooms:
              type: number
            updated_at:
              type: string
            user_id:
              type: string
          example:
            __class__: "Place"
            city_id: "0f7e8c95-d238-42b3-aa27-a7bc7c06cf5d"
            created_at: "2022-05-31T20:42:53.350872"
            description: "The best option, you can walk through the beautiful
            gardens, it has air conditioning and a bathtub to take a nice
            bath as you like."
            id: "e311439a-c4ab-451a-848b-3db2648090df"
            latitude: 37.774
            longitude: -122.431
            max_guest: 6
            name: "Lovely Place"
            number_bathrooms: 3
            number_rooms: 1
            price_by_night: 120
            updated_at: "2022-05-31T20:42:53.350872"
            user_id: "031f949b-750e-49d0-b088-602abeebc47c"
      400:
        description: User error
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Missing name"
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    new_place = request.get_json()
    if not new_place:
        abort(400, 'Not a JSON')
    if 'user_id' not in new_place:
        abort(400, 'Missing user_id')
    if not storage.get(User, new_place['user_id']):
        abort(404)
    if 'name' not in new_place:
        abort(400, 'Missing name')
    new_place['city_id'] = city_id
    place = Place(**new_place)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def place_id_put(place_id):
    """
    Updates a Place object
    ---
    tags:
      - Place
    parameters:
      - name: place_id
        in: path
        required: true
      - name: update_place
        description: Place's information to be updated
        in: body
        required: true
        example:
          {
            "name": "Hacienda Nápoles"
          }
    responses:
      200:
        description: Place updated
        schema:
          type: object
          properties:
            __class__:
              type: string
            city_id:
              type: string
            created_at:
              type: string
            description:
              type: string
            id:
              type: string
            latitude:
              type: number
            longitude:
              type: number
            max_guest:
              type: number
            name:
              type: string
            number_bathrooms:
              type: number
            number_rooms:
              type: number
            updated_at:
              type: string
            user_id:
              type: string
          example:
            __class__: "Place"
            city_id: "d96b80e3-2c05-4fb6-922e-36643005a530"
            created_at: "2017-03-25T02:17:06.000000"
            description: "Completely renovated quality 31-foot Airstream [...]"
            id: "30e56424-c0f0-4e36-9523-f5e904bb3142"
            latitude: 38.3127
            longitude: -122.294
            max_guest: 2
            name: "Hacienda Nápoles"
            number_bathrooms: 1
            number_rooms: 1
            price_by_night: 130
            updated_at: "2021-09-22T15:06:41.520104"
            user_id: "61302be9-4b31-4be0-92fc-d0dda253e167"
      400:
        description: Invalid JSON
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not a JSON"
      404:
        description: No place found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not found"
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    request_json = request.get_json()
    if not request_json:
        abort(400, 'Not a JSON')
    for key, value in request_json.items():
        if key != 'id' and key != 'user_id' and key != 'city_id' \
                and key != 'created_at' and key != 'updated_at':
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
