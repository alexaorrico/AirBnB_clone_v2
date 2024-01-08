#!/usr/bin/python3
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET"], strict_slashes=False)
def retrieve_reviews(place_id):
    """Retrieves list of all Review Objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = storage.all(Review).values()
    place_reviews = [
        review.to_dict() for review in reviews if review.place_id == place_id
    ]
    return jsonify(place_reviews)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review(review_id):
    """Retrieves Review object based on the id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews",
                 methods=["POST"], strict_slashes=False)
def create_review(place_id):
    """Creates a Review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    if "text" not in data:
        abort(400, "Missing text")

    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)

    data["place_id"] = place_id
    new_review = Review(**data)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key not in {"id", "user_id", "place_id",
                       "created_at", "updated_at"}:
            setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict()), 200
