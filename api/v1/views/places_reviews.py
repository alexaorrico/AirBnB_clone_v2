#!/usr/bin/python3
"""Flask application for Review class/entity"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from flask import jsonify, abort, request


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET"], strict_slashes=False)
def retrieves_all_reviews(place_id):
    """Returns the list of all Reviews objects"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = place.reviews
    reviews_list = []
    for review in reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_reviews(review_id):
    """Returns an object by id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes an object by id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews",
                 methods=["POST"], strict_slashes=False)
def create_review(place_id):
    """Creates an object"""
    review_data = request.get_json()
    if not review_data:
        abort(400, 'Not a JSON')

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if "user_id" not in review_data.keys():
        abort(400, "Missing user_id")

    user = storage.get(User, review_data.get("user_id"))
    if not user:
        abort(404)

    if "text" not in review_data.keys():
        abort(400, "Missing text")

    review_data["place_id"] = place_id
    new_review = Review(**review_data)
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """Updates an object"""
    review_data = request.get_json()
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    elif not review_data:
        abort(400, "Not a JSON")

    for key, value in review_data.items():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
