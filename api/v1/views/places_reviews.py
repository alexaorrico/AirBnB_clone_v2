#!/usr/bin/python3
"""Cities API actions"""

from flask import Flask, jsonify
from flask import abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    """retrieve a list of all cities"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route("/reviews/<review_id>", methods=['GET'], strict_slashes=False)
def get_review_by_id(review_id):
    """CIty objects based on city id, else 404"""
    review = storage.get("Review", review_id)
    if review:
        result = review.to_dict()
        return jsonify(result)
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ CIty objects based on city id, else 404"""
    review = storage.get("Review", review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """CIty objects based on state id, else 404"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    user_id = request.json['user_id']
    if 'text' not in request.get_json():
        abort(400, 'Missing text')
    all_places = storage.all("Place").values()
    place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
    if place_obj == []:
        abort(404)
    all_users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in all_users if obj.id == user_id]
    if user_obj == []:
        abort(404)
    reviews = []
    new_review = Review(text=request.json['text'], place_id=place_id,
                        user_id=user_id)
    storage.new(new_review)
    storage.save()
    reviews.append(new_review.to_dict())
    return jsonify(reviews[0]), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ CIty objects based on city id, else 404"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)

    update = request.get_json()
    if not update:
        abort(400, "Not a JSON")

    keys_to_exclude = ["id", "place_id", "user_id", "created_at", "updated_at"]
    for key in keys_to_exclude:
        update.pop(key, None)

    for key, value in update.items():
        setattr(review, key, value)

    storage.save()
    result = review.to_dict()
    return make_response(jsonify(result), 200)
