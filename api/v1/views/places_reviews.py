#!/usr/bin/python3
"""This module implement a rule that return a view"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User
from flasgger.utils import swag_from


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
@swag_from('documentation/reviews/get_reviews.yml', methods=['GET'])
def review_by_place(place_id):
    """View function that return Review objects by Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
@swag_from('documentation/reviews/get_review.yml', methods=['GET'])
def show_review(review_id):
    """Endpoint that return a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
@swag_from('documentation/reviews/delete_reviews.yml', methods=['DELETE'])
def delete_review(review_id):
    """Endpoint that delete a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
@swag_from('documentation/reviews/post_reviews.yml', methods=['POST'])
def insert_review(place_id):
    """Endpoint that insert a Review object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    res = request.get_json()
    if type(res) != dict:
        abort(400, description="Not a JSON")
    if not res.get("user_id"):
        abort(400, description="Missing user_id")
    res['place_id'] = place_id
    user = storage.get(User, res.get('user_id'))
    if user is None:
        abort(404)
    if not res.get("text"):
        abort(400, description="Missing text")
    new_review = Review(**res)
    new_review.place_id = place_id
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
@swag_from('documentation/reviews/put_reviews.yml', methods=['PUT'])
def update_review(review_id):
    """Endpoint that update a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    res = request.get_json()
    if type(res) != dict:
        abort(400, description="Not a JSON")
    for key, value in res.items():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
