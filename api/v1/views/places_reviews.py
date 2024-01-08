#!/usr/bin/python3
""" module view for place reviewobjects;
handles all default Restful API actions
"""
from flask import Flask, jsonify, request, abort
from models import storage
from models.review import Review
from models.place import Place
from . import app_views
import uuid


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    """gets list of all Review objects"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = place.reviews
    reviewss = [review.to_dict() for review in reviews]
    return jsonify(reviewss)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id=None):
    """get review by id"""

    # print("Full request: ", request)
    review = storage.get(Review, review_id)
    # print('State id is {}'.format(state_id))
    # print('State id is type {}'.format(type(state_id)))
    # print('State is {}'.format(state))

    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(city_id):
    """deletes a review identified by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(review_id):
    """create review from http request"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')

    user = storage.get("User", data['user_id'])
    if user is None:
        abort(404)
    if 'text' not in data:
        abort(400, 'Missing text')

    data['place_id'] = place.id
    review = Review(**data)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """updates a review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, val in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(review, key, val)
    review.save()
    return jsonify(review.to_dict()), 200
