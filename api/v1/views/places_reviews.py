#!/usr/bin/python3
""""view for Review objects that handles all RESTFul API actions"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET", "POST"])
def get_place_review(place_id=None):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    if request.method == "GET":
        all_reviews = [review.to_dict() for review in storage.all(
            Review).values() if review.place_id == place.id]
        return jsonify(all_reviews), 200

    review_data = request.get_json(silent=True)
    if review_data is None:
        abort(400, "Not a JSON")
    if "user_id" not in review_data:
        abort(400, "Missing user_id")
    if "text" not in review_data:
        abort(400, "Missing text")

    user = storage.get("User", review_data["user_id"])
    if not user:
        abort(404)
    new_review = Review(place_id=place.id,
                        user_id=review_data["user_id"],
                        text=review_data["text"])
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["GET", "DELETE", "PUT"])
def get_review(review_id):
    """Retrieves a Review object"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)

    if request.method == "GET":
        return jsonify(review.to_dict()), 200

    if request.method == "DELETE":
        storage.delete(review)
        storage.save()
        return jsonify({}), 200

    review_data = request.get_json(silent=True)
    if not review_data:
        abort(400, "Not a JSON")
    ignore_attrs = ["id", "user_id", "place_id", "created_at", "updated_at"]
    [setattr(review, key, val)
     for key, val in review_data.items() if key not in ignore_attrs]

    return jsonify(review.to_dict()), 200
