#!/usr/bin/python3
"""
a new view for Place objects that handles
all default RESTFul API actions:
"""


from api.v1.views import app_views
from flask import Flask, make_response, jsonify, request
from models import storage
from models.user import User
from models.place import Place
from models.review import Review
from werkzeug.exceptions import BadRequest, NotFound


@app_views.route(
    '/places/<place_id>/reviews',
    methods=['GET'],
    strict_slashes=False
)
def all_reviews(place_id):
    """
    he list of all Place objects of a City:

    Args:
        place_id : ID of the specified City object.

    Raises:
        NotFound: Raises a 404 error if place_id
        is not linked to any User object.

    Returns:
        json: Wanted Place object with status code 200.
    """
    place = storage.all(Place, place_id)
    review_list = []

    if place is None:
        raise NotFound

    reviews = place.reviews

    for review in reviews.items():
        review_list.append(review.to__dict())
    return make_response(jsonify(review_list), 200)


@app_views.route(
    '/reviews/<review_id>',
    methods=['GET'],
    strict_slashes=False
)
def single_review(review_id):
    """
    Retrieves a specified Review object.

    Args:
        review_id : ID of the specified Review object.

    Raises:
        NotFound: Raises a 404 error if review_id
        is not linked to any Review object.

    Returns:
        json: Wanted Review object with status code 200.
    """
    review = storage.get(Review, review_id)

    if review is None:
        raise NotFound

    return make_response(jsonify(review.to__dict()), 200)


@app_views.route(
    '/reviews/<review_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def delete_review(review_id):
    """
    Deletes a specified Review object.

    Args:
        review_id : ID of the wanted Review object.

    Raises:
        NotFound: Raises a 404 error if review_id
        is not linked to any Review object.

    Returns:
        json: Empty dictionary with the status code 200.
    """

    review = storage.get(Review, review_id)

    if review is None:
        raise NotFound

    storage.delete(review)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route(
    '/places/<place_id>/reviews',
    methods=['POST'],
    strict_slashes=False
)
def add_review(place_id):
    """
    Creates a new Review object.

    Error cases:
        BadRequest: If the given data is not a
        valid json or if the key 'name' is not
        present sends status code 400.

    Returns:
        json: The new Review with the status code 201.
    """
    place = storage.get(Place, place_id)

    if place is None:
        raise NotFound

    if not request.json:
        return make_response('Not a JSON', 400)

    if 'user_id' not in request.get_json().keys():
        return make_response('Missing user_id', 400)

    user = storage.get(User, request.get_json()['user_id'])

    if user is None:
        raise NotFound

    if 'text' not in request.get_json().keys():
        return make_response('Missing text', 400)

    data = request.get_json()
    data['place_id'] = place_id
    review = Review(**data)

    review.save()

    return make_response(jsonify(review.to_dict()), 201)


@app_views.route(
    '/reviews/<review_id>',
    methods=['PUT'],
    strict_slashes=False
)
def update_review(review_id):
    """
    Update a specified  Review object.

    Args:
        review_id : Id of the wanted A Review object.

    Returns:
        json: The updated Review object with the status code 200.
    """
    review = storage.get(Review, review_id)

    if not request.get_json:
        return make_response('Not a JSON', 400)

    if review is None:
        raise NotFound

    for key, rvw in request.get_json().items():
        if key not in ('id', 'created_at', 'updated_at'):
            review.__setattr__(key, rvw)

    review.save()

    return make_response(jsonify(review.to__dict()), 200)
