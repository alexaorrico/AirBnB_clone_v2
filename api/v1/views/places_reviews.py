#!/usr/bin/python3
"""The `places_reviews` module"""


from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET"], strict_slashes=False)
def list_all_reviews(place_id):
    """Lists all reviws by place_id"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify([places.to_dict() for places in place.reviews])


@app_views.route("/reviews/<review_id>",
                 methods=["GET"], strict_slashes=False)
def list_review_id(review_id):
    """Retrives a review by review_id"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    """Deletes a review by id"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews",
                 methods=["POST"], strict_slashes=False)
def create_review(place_id):
    """Creates a review by place_id"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    payload = request.get_json()
    if not payload:
        abort(400, "Not a JSON")
    if "user_id" not in payload:
        abort(400, "Missing user_id")
    user = storage.get("User", payload["user_id"])
    if not user:
        abort(404)
    if "text" not in payload:
        abort(404, "Missing text")
    new_review = Review(**payload)
    setattr(new_review, "place_id", place_id)
    storage.new(new_review)
    storage.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route("/reviews/<review_id>",
                 methods=["PUT"], strict_slashes=False)
def update_review_id(review_id):
    """Updates review by id"""
    review = storage.get("Review", review_id):
        if not review:
            abort(404)
    payload = request.get_json()
    if not payload:
        abort(400, "Not a JSON")
    for key, value in payload.items():
        if key not in {"id", "user_id",
                       "place_id", "created_at", "updated_at"}:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
