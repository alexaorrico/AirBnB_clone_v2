#!/usr/bin/python3
""" view for Review objects that handles all default RESTFul API actions """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def places_place_id_reviews(place_id):
    """Retrieves all Review objects of a Place"""

    place_catch = storage.get('Place', place_id)

    # If the place_id is not linked to any Place object, raise a 404 error
    if place_catch is None:
        abort(404)

    # retrieves Review object
    if request.method == 'GET':
        reviews = storage.all(Review)
        reviews_list = []
        for review in reviews.values():
            reviews_dict = review.to_dict()
            if reviews_dict['place_id'] == place_id:
                reviews_list.append(reviews_dict)
        return jsonify(reviews_list)

    elif request.method == 'POST':
        # transform the HTTP body request to a dictionary
        body_request_dict = request.get_json()

        # If the HTTP body request is not valid JSON
        if not body_request_dict:
            abort(400, 'Not a JSON')

        # If the dictionary doesn’t contain the key user_id
        if 'user_id' not in body_request_dict:
            abort(400, 'Missing user_id')

        user_catch = storage.get('User', body_request_dict['user_id'])

        # If the user_id is not linked to any User object, raise a 404 error
        if user_catch is None:
            abort(404)

        # If the dictionary doesn’t contain the key text
        if 'text' not in body_request_dict:
            abort(400, 'Missing text')

        # create new object Review with body_request_dict
        body_request_dict['place_id'] = place_id
        new_review = Review(**body_request_dict)

        storage.new(new_review)
        storage.save()
        return new_review.to_dict(), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def review_id(review_id):
    """Retrieves Review object"""
    review_catch = storage.get(Review, review_id)

    # If the review_id is not linked to any Review object, raise a 404 error
    if review_catch is None:
        abort(404)

    # Retrieves a Review object
    if request.method == 'GET':
        return review_catch.to_dict()

    # Deletes a Review object
    if request.method == 'DELETE':
        empty_dict = {}
        storage.delete(review_catch)
        storage.save()
        return empty_dict, 200

    # update a Review object
    if request.method == 'PUT':
        # transform the HTTP body request to a dictionary
        body_request_dict = request.get_json()

        # If the HTTP body request is not valid JSON
        if not body_request_dict:
            abort(400, 'Not a JSON')

        # Update the Review object with all key-value pairs of the dictionary
        # Ignore keys: id, user_id, place_id, created_at and updated_at

        for key, value in body_request_dict.items():
            if key not in ['id', 'user_id', 'place_id', 'created_at',
                           'updated_at']:
                setattr(review_catch, key, value)

        review_catch.save()
        return review_catch.to_dict(), 200
