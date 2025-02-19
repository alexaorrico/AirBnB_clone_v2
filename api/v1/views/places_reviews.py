#!/usr/bin/python3
"""review.py"""

from flask import jsonify
from flask import abort
from flask import request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place


@app_views.route("/places/<string:place_id>/reviews", strict_slashes=False)
def get_reviews_of_place(place_id=None):
    """retrieves all reviews """
    if storage.get(Place, place_id) is None:
        abort(404)

    reviews = storage.get(Place, place_id).reviews

    return jsonify(reviews), 200


@app_views.route("/reviews/<string:review_id>")
def get_review(review_id=None):
    """retrieves a specific review """
    if review_id is None:
        abort(404)

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<string:review_id>", methods=['DELETE'])
def delete_review(review_id=None):
    """retrieves a specific review """
    if review_id is None:
        abort(404)

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    return {}, 200


@app_views.route(
        "/places/<string:place_id>/reviews",
        methods=['POST'],
        strict_slashes=False)
def create_review(place_id=None):
    """ Creates a review"""
    if storage.get(Place, place_id) is None:
        return jsonify({"error": "Not found"}), 404

    review_dict = None
    try:
        review_dict = request.get_json()
        if not isinstance(review_dict, dict):
            raise ValueError
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in review_dict:
        return jsonify({"error": "Missing user_id"}), 400
    if 'text' not in review_dict:
        return jsonify({"error": "Missing text"}), 400

    review = Review(
            text=review_dict['text'],
            place_id=place_id,
            user_id=review_dict['user_id']
    )

    for key, val in review_dict.items():
        setattr(review, key, val)

    storage.new(review)
    storage.save()

    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'], strict_slashes=False)
def update_review(review_id=None):
    """ updates a review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    review_dict = None
    try:
        review_dict = request.get_json()
        if not isinstance(review_dict, dict):
            raise ValueError
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    for key, val in review_dict.items():
        if key not in [
            'id', 'user_id', 'place_id', 'created_at', 'updated_at'
        ]:
            setattr(review, key, val)

    storage.save()
    return jsonify(review.to_dict()), 200
