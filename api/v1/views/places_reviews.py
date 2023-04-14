#!/usr/bin/python3
"""
create a new view that handles all default RESTFul API actions
"""
from models.review import Review
from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_places(place_id):
    """retrieve the list of all City objects"""
    # retrieve states and IDs registered in the State class
    place = storage.get(Place, place_id)
    # raise an error if the state_id is not linked to any State object
    if place is None:
        abort(404)
    else:
        list_reviews = [place.to_dict() for place in place.reviews]
        return jsonify(list_reviews)


@app_views.route('reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_place(review_id):
    """retrieve a City object"""
    # retrieve City objects and their IDs registered in the City class
    review = storage.get(Review, review_id)

    # raise an error if the city_id is not linked to any City object
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(review_id):
    """delete a City object"""
    # retrieve all City objects registered in the City class
    review = storage.get(Review, review_id)

    # raise an error if the city_id doesn't match
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    # return an empty dictionary with the status code 200
    return (jsonify({}), 200)


@app_views.route('places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_place(place_id):
    """create a city object"""
    # get State object which is linked to the state_id
    place = storage.get(Place, place_id)
    # raise an error if the state_id is not linked to any State object
    if place is None:
        abort(404)

    # transform the HTTP body request to a dictionary
    body = request.get_json()
    # raise error if the the HTTP body request is not a valid JSON
    if body is None:
        abort(400, 'Not a JSON')

    # raise error if the dictionary doesn’t contain the key name
    if 'name' not in body:
        abort(400, 'Missing name')

    body['place_id'] = place_id
    review = Review(**body)
    storage.new(review)
    place.save()
    return (jsonify(review.to_dict()), 201)


@app_views.route('reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_place(review_id):
    """update a City object"""
    # get a City object and its ID
    review = storage.get(Review, review_id)
    # raise error id city_id is not linked to any City object
    if review is None:
        abort(404)

    # transform the HTTP body request to a dictionary
    body = request.get_json()
    # raise error if the the HTTP body request is not a valid JSON
    if body is None:
        abort(400, 'Not a JSON')

    ignore_key = ['id', 'state_at', 'created_at' 'updated_at']
    for key, value in body.items():
        if key not in ignore_key:
            setattr(review, key, value)

    storage.save()
    return (jsonify(review.to_dict()), 200)
