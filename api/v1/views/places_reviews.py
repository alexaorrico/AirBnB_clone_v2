#!/usr/bin/python3
"""
    API module places_reviews
"""

import models
from models import storage
from models.place import *
from models.user import *
from models.review import *

from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review_reviews(place_id):
    """
        A function that Retrieves the list of all Review
        of a place: GET /api/v1/places/<Review_id>/reviews
    """
    # get place by id
    place = storage.get(Place, place_id)

    # get Review from places, save in list and return
    if (place):
        placeReviews = [review.to_dict() for review in place.reviews]

        return jsonify(placeReviews)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """
        A function that Retrieves a Review object:
        GET /api/v1/places/<place_id>
    """
    # get review by id
    obj = storage.get(Review, review_id)

    # return review object dictionary if found
    if (obj):
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_review(review_id):
    """
        A function that Deletes a Review object:
        DELETE /api/v1/places/<place_id>
    """
    # get review object by id
    obj = storage.get(Review, review_id)

    # is place is found, delete object, save and return {}
    if (obj):
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def add_review(place_id):
    """
        A function that Creates a Review:
        POST /api/v1/places/<place_id>/reviews
    """
    place = storage.get(Place, place_id)

    if (place):
        # get json sting
        json_str = request.get_json()

        # Error handling and missing info
        # Check If the HTTP body request is not valid JSON
        if (not json_str):
            abort(400, 'Not a JSON')
        if ('user_id' not in json_str):
            abort(400, 'Missing user_id')
        if ('text' not in json_str):
            abort(400, 'Missing text')

        # get | create user object from json string
        user = storage.get(User, json_str['user_id'])
        if (not user):
            abort(404)

        json_str['place_id'] = place_id

        obj = Review(**json_str)

        obj.save()

        return jsonify(obj.to_dict()), 201
    else:
        abort(404)


@app_views.route('reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """
        A function that Updates a Review object:
        PUT /api/v1/reviews/<review_id>
    """
    # get the review by id
    obj = storage.get(Review, review_id)

    if (obj):
        json_str = request.get_json()
        # Check If the HTTP body request is not valid JSON
        if (not json_str):
            abort('400', 'Not a JSON')

        # Update Review objects attributes
        to_ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, value in json_str.items():
            if key not in to_ignore:
                setattr(obj, key, value)

        #  save and return
        obj.save()

        return jsonify(obj.to_dict()), 200
    else:
        abort(404)
