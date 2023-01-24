#!/usr/bin/python3
"""Place Reviews API"""
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from . import app_views
from flask import jsonify, abort, request

@app_views.route("/places/<place_id>/reviews")
def reviews(place_id):
    """Get all place reviews"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = place.reviews
    review_list = []
    for review in reviews:
        review_list.append(review.to_dict())
    return jsonify(review_list)

@app_views.route("/reviews/<review_id>")
def review(review_id):
    """Get a single review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())

@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """Delete a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return  jsonify({})

@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_review(place_id):
    """Create a place review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    data = request.get_json()
    if "user_id" not in data:
        abort(400, "Missing user_id")
    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)
    if "text" not in data:
        abort(400, "Missing text")
    data["place_id"] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201

@app_views.route("/reviews/<review_id>", methods=["PUT"])
def update_review(review_id):
    """Update a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    data = request.get_json()
    if "id" in data:
        data.pop("id")
    if "place_id" in data:
        data.pop("city_id")
    if "user_id" in data:
        data.pop("user_id")
    if "created_at" in data:
        data.pop("created_at")
    if "updated_at" in data:
        data.pop("updated_at")
    for key, value in data.items():
        review.__setattr__(key, value)
    review.save()
    return jsonify(review.to_dict())
