#!/usr/bin/python3
"""Place"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_places_reviews(place_id):
    """Gets the list of all places reviews"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = [review.to_dict() for review in place.reviews]
    return jsonify(data)


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieves a review object"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a review object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    new_review_data = request.get_json()
    if not new_review_data:
        abort(400, "Not a JSON")
    if "user_id" not in new_review_data:
        abort(400, "Missing user_id")
    user = storage.get(User, new_review_data['user_id'])
    if not user:
        abort(404)
    if "text" not in new_review_data:
        abort(400, "Missing text")
    new_review_data["place_id"] = place_id
    new_review = Review(**new_review_data)
    new_review.save()
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a review by id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    data_to_update = request.get_json()
    if not data_to_update:
        abort(400, "Not a JSON")
    for key, value in data_to_update.items():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes review object base on id"""
    review = storage.get(Review, review_id)
    if review:
        review.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)
