#!/usr/bin/python3
"""Reviews RESTAPI"""
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route("/places/<place_id>/reviews", strict_slashes=False)
def get_reviews(place_id):  # Get all reviews of a place
    place = storage.get(Place, place_id)
    if place:
        return jsonify([review.to_dict() for review in place.reviews])
    abort(404)


@app_views.route("/reviews/<review_id>", strict_slashes=False)
def get_review(review_id):  # get a specific review
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route("/reviews/<review_id>/",
                 strict_slashes=False, methods=["DELETE"])
def delete_review(review_id):  # Delete a review
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False, methods=["POST"])
def create_review(place_id):  # Create a review about a place
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if "user_id" not in data:
        abort(400, description="Missing user_id")
    if "name" not in data:
        abort(400, description="Missing name")
    if "text" not in data:
        abort(400, description="Missing text")
    user = storage.get(User, data.get('user_id'))
    if not user:
        abort(404)
    new_review = Review(**data)
    new_review.place_id = place_id
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=["PUT"])
def update_review(review_id):  # Update a review
    review = storage.get(Review, review_id)
    if review:
        data = request.get_json()
        if not data:
            abort(400, description="Not a JSON")
        ignorables = ["id", "created_at", "updated_at", "user_id", "place_id"]
        for key, value in data.items():
            if key not in ignorables:
                setattr(review, key, value)
        storage.save()
        return make_response(jsonify(review.to_dict()), 200)
    abort(404)
