#!/usr/bin/python3
""" """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.place import Place
from models.review import Review
from models import storage
PL = '/places/<place_id>/reviews'
RV = '/reviews/<review_id>'
IGNORED_KEYS = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']


@app_views.route(PL, methods=['GET'], strict_slashes=False)
def get_reviews_from_place(place_id):
    """ """
    reviews = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify([review.to_dict() for review in places.reviews])


@app_views.route(RV, methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(PL, methods=['POST'], strict_slashes=False)
def create_review_for_place(place_id):
    """ """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.json:
        abort(404, "Not a JSON")

    data = request.get_json()

    if "user_id" not in data:
        abort(400, "Missing user_id")

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    if "text" not in data:
        abort(400, "Missing text")

    data['place_id'] = place_id
    new_review = Review(**data)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route(RV, methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.is_json:
        abort(400, "Not a json")

    data = request.get_json()
    for key, value in data.items():
        if key not in IGNORED_KEYS:
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict()), 200


@app_views.route(RV, methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """ """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({}), 200
