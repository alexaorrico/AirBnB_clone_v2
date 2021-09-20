#!/usr/bin/python3
"""module for Review view"""
from flask import abort, request, jsonify, make_response
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views


@app_views.route("/places/<string:place_id>/reviews", strict_slashes=False, methods=["GET"])
def get_place_reviews(place_id):
    """retrives reviews"""
    required_place = storage.get(Place, place_id)
    if (not required_place):
        abort(404)
    result = []
    for review in required_place.reviews:
        result.append(review.to_dict())
    return jsonify(result)


@app_views.route("/reviews/<string:review_id>", strict_slashes=False, methods=["GET"])
def get_review(review_id):
    """retrives a review"""
    required_review = storage.get(Review, review_id)
    if (not required_review):
        abort(404)
    return jsonify(required_review.to_dict())


@app_views.route("/reviews/<string:review_id>", strict_slashes=False, methods=["DELETE"])
def delete_review(review_id):
    """deletes a review"""
    required_review = storage.get(Review, review_id)
    if (not required_review):
        abort(404)
    storage.delete(required_review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<string:place_id>/reviews", strict_slashes=False, methods=["POST"])
def create_review(place_id):
    """creates a new review"""
    required_place = storage.get(Place, place_id)
    if (not required_place):
        abort(404)
    if not request.json:
        return make_response("Not a JSON", 400)
    if not 'user_id' in request.json:
        return make_response("Missing user_id", 400)

    properties = request.get_json()
    required_user = storage.get(User, properties["user_id"])
    if (not required_user):
        abort(404)

    if not 'text' in request.json:
        return make_response("Missing text", 400)

    properties["place_id"] = place_id
    new_review = Review(**properties)
    new_review.save()
    return new_review.to_dict(), 201


@app_views.route("/reviews/<string:review_id>", strict_slashes=False, methods=["PUT"])
def edit_review(review_id):
    """edits a review"""
    required_review = storage.get(Review, review_id)
    if (not required_review):
        abort(404)
    if not request.json:
        return make_response("Not a JSON", 400)

    input_dict = request.get_json()
    for key, value in input_dict.items():
        if not (key in ["id", "created_at", "updated_at", "user_id", "place_id"]):
            if (hasattr(required_review, key)):
                setattr(required_review, key, value)
    required_review.save()
    return required_review.to_dict(), 200
