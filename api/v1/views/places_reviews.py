#!/usr/bin/python3
"""RESTful API for class Review"""

from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request
from flasgger.utils import swag_from


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
@swag_from('documentation/review/get_reviews.yml', methods=['GET'])
def get_reviews(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/review/get_review.yml', methods=['GET'])
def get_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/review/delete_review.yml', methods=['DELETE'])
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
@swag_from('documentation/review/post_review.yml', methods=['POST'])
def post_review(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    res = request.get_json()
    if not res:
        return abort(400, description="Not a JSON")
    if 'user_id' not in res:
        return abort(400, description="Missing user_id")
    if 'text' not in res:
        return abort(400, description="Missing text")
    user = storage.get(User, res['user_id'])
    if not user:
        return abort(404)
    res['place_id'] = place_id
    new_review = Review(**res)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/review/put_review.yml', methods=['PUT'])
def put_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    res = request.get_json()
    if not res:
        return abort(400, description="Not a JSON")
    for key, value in res.items():
        if key not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200

