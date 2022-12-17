#!/usr/bin/python3
"""Module for review endpoints"""
from flask import jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def get_places_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        return make_response(jsonify({"error": "Not found"}), 404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_reviews(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        return make_response(jsonify({"error": "Not found"}), 404)
    return jsonify(review.to_dict())


@app_views.route('reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        return make_response(jsonify({"error": "Not found"}), 404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("places/<place_id>/reviews",
                 strict_slashes=False, methods=["POST"])
def post_review(place_id):
    """POST /place API route"""
    place = storage.get(Place, place_id)
    if not place:
        return make_response(jsonify({"error": "Not found"}), 404)

    data = request.get_json(force=True, silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "text" not in data:
        return make_response(jsonify({"error": "Missing text"}), 400)
    if "user_id" not in data:
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    user = storage.get(User, data["user_id"])
    if not user:
        return make_response(jsonify({"error": "Not found"}), 404)

    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def put_review(review_id):
    """PUT /place API route"""
    review = storage.get(Review, review_id)
    if not review:
        return make_response(jsonify({"error": "Not found"}), 404)
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(review, key, value)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
