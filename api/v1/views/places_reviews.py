#!/usr/bin/python3
"""This Module contains the api for the reviews"""
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User
from models import storage
from flask import abort, jsonify, request


@app_views.route("/places/<place_id>/reviews", strict_slashes=True, methods=["GET"])
def get_place_reviews(place_id=None):
    """This Method retrieves the reviews based on the place_id"""
    if not place_id:
        abort(404)
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews()]
    return jsonify(reviews), 200


@app_views.route("/api/v1/reviews/<review_id>", strict_slashes=True, methods=["GET"])
def get_reviews(review_id=None):
    """This Method retrieves review based on the review_id"""
    if not review_id:
        abort(404)
    review = storage.get(Review, review_id)
    if not review:
        abort(review)
    return jsonify(review.to_dict()), 200


@app_views.route("/api/v1/reviews/<review_id>", strict_slashes=True, methods=["DELETE"])
def delete_reviews(review_id=None):
    """This method deletes based on review_id"""
    if not review_id:
        abort(404)
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    return jsonify({}), 200


@app_views.route("/api/v1/places/<place_id>/reviews", strict_slashes=True, methods=["POST"])
def post_review(place_id=None):
    """This Method creates a new review based on the review_id"""
    if request.content_type != "application/json":
        jsonify({"error": "Not a JSON"}), 400
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if "user_id" not in data.keys():
        return jsonify({"error":"Missing user_id"}), 200
    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)
    if "text" not in data.keys():
        return jsonify({"error": "Missing text"}), 400
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/api/v1/reviews/<review_id>", strict_slashes=True, methods=["PUT"])
def put_review(review_id=None):
    """This Method updates the data of review based on the review_id"""
    review = storage.get(Review, review_id)
    if not review_id or review:
        abort(404)
    if request.content_type != "applicatioon/json":
        return jsonify({"error": "Not a JSON"})
    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "user_id", "place_id", "created_at"]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
