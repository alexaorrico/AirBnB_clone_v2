#!/usr/bin/python3
"""
module: Reviews api
"""
from api.v1.views import app_views, storage, Review
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """ returns all reviews got a place in JSON format """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    reviews = [review.to_json() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_single_review(review_id):
    """ returns a review object in JSON format """
    try:
        review = storage.get('Review', review_id)
        return jsonify(review.to_json())
    except:
        abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """ deletes a review  """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """ creates a place review """
    try:
        response = request.get_json()
    except:
        response = None

    if response is None:
        return "Not a JSON", 400
    if 'user_id' not in response.keys():
        return "Missing user_id", 400
    if 'text' not in response.keys():
        return "Missing text", 400

    place = storage.get('Place', place_id)
    user = storage.get('User', response['user_id'])
    if ((place is None) or (user is None)):
        abort(404)

    review = Review(**response)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_json()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """ updates a place review  """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    try:
        response = request.get_json()
    except:
        response = None
    if response is None:
        return "Not a JSON", 400
    for item in ("id", "user_id", "created_at", "updated_at", "place_id"):
        response.pop(item, None)
    for k, v in response.items():
        setattr(review, k, v)
    review.save()
    return jsonify(review.to_json()), 200
