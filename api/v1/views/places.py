#!/usr/bin/python3
""" Handle RESTful API request for places"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.place import Place
from models.user import User


# @app_views.route('/cities/<city_id>/places',
#                  methods=['GET'],
#                  strict_slashes=False)
# def all_places(city_id):
#     """ GET ALL PLACES """

#     # verify if city_id exist if not return 404
#     city = storage.get(City, city_id)
#     if not city:
#         abort(404)
 
#     # list all places
#     places = storage.all(Place).values()

#     # list to return only with places to the city
#     list_places = []

#     # loop to search into places
#     for place in places:
#         values = place.to_dict()
#         # validate if place belongs to request city
#         if values['city_id'] == city_id:
#             list_places.append(place.to_dict())

#     # return  the list of places
#     return jsonify(list_places)


# @app_views.route('/places/<place_id>',
#                  methods=['GET'],
#                  strict_slashes=False)
# def get_places(place_id):
#     """ Retrieves a specific place """
#     # verify if place_id exist if not return 404
#     instance = storage.get(Place, place_id)
#     if not instance:
#         abort(404)
#     return jsonify(instance.to_dict())


# @app_views.route('/places/<place_id>',
#                  methods=['DELETE'],
#                  strict_slashes=False)
# def delete_place(place_id):
#     """delete a place"""
#     obj = storage.get(Place, place_id)
#     if obj:
#         storage.delete(obj)
#         storage.save()
#         return make_response(jsonify({}), 200)
#     else:
#         abort(404)


# @app_views.route('cities/<city_id>/places',
#                  methods=['POST'],
#                  strict_slashes=False)
# def create_place(city_id):
#     """Creates a place """
#     # validate reques type
#     if not request.get_json():
#         abort(400, description="Not a JSON")

#     # convert data request to Dict
#     data = request.get_json()

#     # search if the city_id and user_id exist if not return 404
#     city = storage.get(City, city_id)
#     user = storage.get(User, data['user_id'])
#     if not city or not user:
#         abort(404)

#     # update data dict with city_id
#     data['city_id'] = city_id

#     # validate requiered attributes
#     if 'name' not in data:
#         abort(400, description="Missing name")
#     if 'user_id' not in data:
#         abort(400, description="Missing user_id")

#     # create a new_instance of class and saves
#     new_instance = Place(**data)
#     new_instance.save()

#     return make_response(jsonify(new_instance.to_dict()), 201)


# @app_views.route('/places/<place_id>',
#                  methods=['PUT'],
#                  strict_slashes=False)
# def update_place(place_id):
#     """update a place"""
#     # validate reques type
#     if not request.get_json():
#         abort(400, description="Not a JSON")

#     # call the object and verify if exist if not return 404
#     obj = storage.get(Place, place_id)
#     if not obj:
#         abort(404)
#     # loads request
#     data = request.get_json()
#     # fields to ignore from update
#     ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

#     # update the data
#     data = request.get_json()
#     for key, value in data.items():
#         if key not in ignore:
#             setattr(obj, key, value)
#     # save update
#     obj.save()

#     return make_response(jsonify(obj.to_dict()), 200)

@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """
    Retrieves the list of all Place objects of a City
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    places = [place.to_dict() for place in city.places]

    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a Place object
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Place Object
    """

    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """
    Creates a Place
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    data = request.get_json()
    user = storage.get(User, data['user_id'])

    if not user:
        abort(404)

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data["city_id"] = city_id
    instance = Place(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """
    Updates a Place
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
