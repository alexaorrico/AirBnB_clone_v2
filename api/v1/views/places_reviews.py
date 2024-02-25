#!/usr/bin/python3
"""Reviews hanlders."""

from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route(
    "/places/<string:place_id>/reviews", methods=["GET"], strict_slashes=False
)
def get_reviews(place_id):
    """Retrieve all the reviews of the specified place."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route(
    "/reviews/<string:review_id>",
    methods=["GET"],
    strict_slashes=False,
)
def get_review(review_id):
    """Get info about specified review."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
    "/reviews/<string:review_id>", methods=["DELETE"], strict_slashes=False
)
def delete_review(review_id):
    """Delete specified review."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route(
    "/places/<string:place_id>/reviews", methods=["POST"], strict_slashes=False
)
def create_review(place_id):
    """Create a new review."""
    req = request.get_json(silent=True)
    if not req:
        abort(400, "Not a JSON")
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if "user_id" not in req:
        abort(400, "Missing user_id")
    user = storage.get(User, req["user_id"])
    if user is None:
        abort(404)
    if "text" not in req:
        abort(400, "Missing text")
    req["place_id"] = place_id
    review = Review(**req)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route(
    "/reviews/<string:review_id>", methods=["PUT"], strict_slashes=False
)
def update_review(review_id):
    """Update specified review."""
    req = request.get_json(silent=True)
    if not req:
        abort(400, "Not a JSON")
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    for attr, val in req.items():
        if attr not in [
            "id",
            "created_at",
            "updated_at",
            "place_id",
            "user_id",
        ]:
            setattr(review, attr, val)
    review.save()
    return jsonify(review.to_dict())
