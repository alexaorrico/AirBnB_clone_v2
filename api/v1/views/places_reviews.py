#!/usr/bin/python3
"""Place_reviews module"""
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.user import User
from models.place import Place
from flask import jsonify, request, abort


@app_views.route("/places/<place_id>/reviews", methods=["GET"])
def get_reviews_from_place(place_id):
    """Gets all review objects of a Place"""
    if storage.get(Place, place_id) is None:
        abort(404)
    return jsonify(([review.to_dict() for review in storage.all(
        Review).values() if review.place_id == place_id]))


@app_views.route("/reviews/<review_id>", methods=["GET"])
def get_review_id(review_id):
    """Gets a review object"""
    if storage.get(Review, review_id) is None:
        abort(404)
    return (jsonify(storage.get(Review, review_id).to_dict()))


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """Deletes a Review based on id"""
    review_object = storage.get(Review, review_id)
    if review_object is None:
        abort(404)
    else:
        storage.delete(review_object)
        storage.save()
        return (jsonify({})), 200


@app_views.route(
    "/places/<place_id>/reviews",
    methods=["POST"],
    strict_slashes=False)
def post_review(place_id):
    """Creates a new review object"""
    if storage.get(Place, place_id) is None:
        abort(404)
    if not request.get_json():
        return (jsonify({"error": "Not a JSON"})), 400
    data = request.get_json()
    if "user_id" not in data:
        return (jsonify({"error": "Missing user_id"})), 400
    if "text" not in data:
        return (jsonify({"error": "Missing text"})), 400
    data["place_id"] = place_id
    new_review_obj = Review(**data)
    new_review_obj.save()
    return jsonify(new_review_obj.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def update_review(place_id):
    """Updates a review object"""
    ignore_data = ["id", "user_id", "city_id", "created_at", "updated_at"]
    data = request.get_json()
    all_the_reviews = storage.get(Place, review_id)
    if all_the_reviews is None:
        abort(404)
    if not data:
        return (jsonify({"error": "Not a JSON"})), 400
    for key, value in data.items():
        if key not in ignore_data:
            setattr(all_the_reviews, key, value)
    storage.save()
    return jsonify(all_the_reviews.to_dict()), 200
