#!/usr/bin/python3
""" places_reviews module for viewing their requests """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def reviews_by_places(place_id=None):
    """ view all reviews by place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews_list = []
    all_reviews = place.reviews
    for review in all_reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route('reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def review_by_id(review_id=None):
    """ view review by id """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id=None):
    """ delete a review by id """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_reviews(place_id=None):
    """ returns a new review with status code 201 """
    requested_json = request.get_json()
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not requested_json:
        abort(400, description="Not a JSON")
    if "user_id" not in requested_json:
        abort(400, description="Missing user_id")
    user = storage.get(User, requested_json.get('user_id'))
    if not user:
        abort(404)
    if "text" not in requested_json:
        abort(400, description="Missing text")
    requested_json["place_id"] = place_id
    new_review = Review(**requested_json)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def put_review(review_id=None):
    """ update a review by id """
    review = storage.get(Review, review_id)
    requested_json = request.get_json()
    if not review:
        abort(404)
    if not requested_json:
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    for key, value in requested_json.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
