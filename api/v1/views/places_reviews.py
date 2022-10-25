#!/usr/bin/python3
"""route for reviews"""
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from flask import abort, jsonify, request, make_response


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=["GET"])
def get_place_review(place_id):
    """retrieves the list of all Review objects of a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    all_place_reviews = []
    for review in place.reviews:
        all_place_reviews.append(review.to_dict())
    return jsonify(all_place_reviews)


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=["POST"])
def post_place_review(place_id):
    """create a new review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "user_id" not in request.get_json():
        abort(400, description="Missing user_id")
    if not storage.get(User, request.get_json()['user_id']):
        abort(404)
    if "text" not in request.get_json():
        abort(400, description="Missing text")
    data = request.get_json()
    new = Review(**data)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["GET"])
def a_review(review_id):
    """Retrieves,Deletes a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if request.method == "GET":
        return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["PUT"])
def put_review(review_id):
    """updates a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    try:
        data = request.get_json()
        if not data:
            abort(400, description="Not a JSON")
    except Exception:
        abort(400, description="Not a JSON")
    ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for attr, val in data.items():
        if attr not in ignore:
            setattr(review, attr, val)
    return jsonify(review.to_dict()), 200
