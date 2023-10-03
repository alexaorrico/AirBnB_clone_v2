#!/usr/bin/python3
"""
This Module contains Place objects that
handles all default RESTFul API actions
"""
from flask import request, abort, jsonify, make_response
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """********"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews_list = [review.to_dict() for review in place.reviews]

    return jsonify(reviews_list)


@app_views.route('reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """**************"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """*****************"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """*********************"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    json_request = request.get_json()
    if not json_request:
        abort(400, 'Not a JSON')

    required_keys = ['user_id', 'text']
    if required_keys[0] not in json_request:
        abort(400, 'Missing user_id')
    if storage.get(User, json_request['user_id']) is None:
        abort(404)
    if required_keys[1] not in json_request:
        abort(400, 'Missing text')
    review = Review(place_id=place_id, **json_request)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """******************"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    json_request = request.get_json()
    if not json_request:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in json_request.items():
        if key is not ignore_keys:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
