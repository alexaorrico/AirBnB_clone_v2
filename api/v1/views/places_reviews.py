#!/usr/bin/python3
"""
Create a new view for Review objects
that handles all default RESTFul API actions
"""
from flask import Flask, jsonify, make_response, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
import json


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET"], strict_slashes=False)
def get_reviews(place_id):
    """
    Retrieves the list of all Review objects of a Place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    reviews_list = [review.to_dict() for review in place.reviews]
    response = make_response(json.dumps(reviews_list, indent=2) + "\n")
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews",
                 methods=["POST"], strict_slashes=False)
def create_review(place_id):
    """Creates a Review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if "user_id" not in request.get_json():
        abort(400, description="Missing user_id")

    data = request.get_json()
    user = storage.get(User, data["user_id"])

    if not user:
        abort(404)

    if "text" not in request.get_json():
        abort(400, description="Missing text")

    new_review = Review(place_id=place_id, **data)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def updata_review(review_id):
    """Updates a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    for k, v in data.items():
        if k not in ["id", "created_at", "place_id", "updated_at"]:
            setattr(review, k, v)

    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
