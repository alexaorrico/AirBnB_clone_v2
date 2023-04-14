#!/usr/bin/python3
"""
create a new view that handles all default RESTFul API actions
"""
from models.review import Review
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_review(place_id):
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
def get_review(review_id):
    """retrieve a City object"""
    # retrieve City objects and their IDs registered in the City class
    review = storage.get(Review, review_id)

    # raise an error if the city_id is not linked to any City object
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
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
def create_review(place_id):
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

    if 'user_id' not in body:
        abort(400, 'Missing user_id')

    user = storage.get(User, body['user_id'])
    if user is None:
        abort(404)

    if 'text' not in body:
        abort(400, 'Missing text')

    body['place_id'] = place_id
    review = Review(**body)
    storage.new(review)
    review.save()
    return (jsonify(review.to_dict()), 201)


@app_views.route('reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
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

    ignore_key = ['id', 'state_at',
                  'created_at' 'updated_at', 'place_id', 'user_id']
    for key, value in body.items():
        if key not in ignore_key:
            setattr(review, key, value)

    storage.save()
    return (jsonify(review.to_dict()), 200)
