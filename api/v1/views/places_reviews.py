#!/usr/bin/python
"""Review API Module"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def show_reviews(place_id):
    """Retrieve a list of reviews for a specific place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    all_reviews = []
    reviews = storage.all(Review).values()
    for review in reviews:
        if review.place_id != place_id:
            continue
        all_reviews.append(review.to_dict())
    return jsonify(all_reviews)
@app_views.route("/reviews/<review_id>", methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieve information about a specific review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete a specific review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """Creates a Review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    post = request.get_json()
    if post is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in post:
        abort(400, 'Missing user_id')
    user = storage.get(User, post['user_id'])
    if user is None:
        abort(404)
    if 'text' not in post:
        abort(400, 'Missing text')
    review = Review(**post)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """Updates a Review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    put = request.get_json()
    if put is None:
        abort(400, 'Not a JSON')
    for k, v in put.items():
        ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        if k not in ignore_keys:
            setattr(review, k, v)
    review.save()
    return jsonify(review.to_dict()), 200
