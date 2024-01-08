#!/usr/bin/python3
"""Create a new view for Place object that
handles all default RESTFul API actions"""
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from flask import jsonify, abort, request


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def getReviewPlace(place_id):
    """method to get reviews of a place"""
    place = storage.get(Place, place_id)
    review_list = [review.to_dict() for review in place.reviews]

    if place is None:
        abort(404)

    return jsonify(review_list), 200


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def get_review(review_id):
    """method to get review"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    return jsonify(review.to_dict()), 200


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """method to delete review"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()

    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """method to create a new review"""
    place = storage.get(Place, place_id)
    data = request.get_json()
    if place is None:
        abort(404)
    if data is None:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)
    if "text" not in data:
        abort(400, "Missing name")
    review = Review(**data)
    review.save()

    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """Method to update a review"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, val in data.items():
        if key in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            continue
        setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict()), 200
