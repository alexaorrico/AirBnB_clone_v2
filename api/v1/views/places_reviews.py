#!/usr/bin/python3
""" Module for review object view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """ Returns all review objects of a place """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    reviews_dict_list = [review.to_dict() for review in place.reviews]
    return jsonify(reviews_dict_list)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review_id(review_id):
    """ Method retrieves review object with certain id """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Method deletes review object based off of its id """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """ Method creates new review object """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    if body.get("user_id") is None:
        abort(400, "Missing user_id")
    if body.get("text") is None:
        abort(400, "Missing text")
    user = storage.get("User", body['user_id'])
    if not user:
        abort(404)
    body['place_id'] = place_id
    review = Review(**body)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """ Method updates a review object based off its id """
    review = storage.get("Review", review_id)
    body = request.get_json()
    if not review:
        abort(404)
    if not body:
        abort(400, "Not a JSON")
    for k, v in body.items():
        if k not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(review, k, v)
    review.save()
    return jsonify(review.to_dict())
