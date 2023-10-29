#!/usr/bin/python3
"""city view"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id):
    """retrieve all reviews of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        reviews_list = []
        for review in place.reviews:
            reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def a_review(review_id):
    """retrieve a review with its id"""
    try:
        review = storage.get(Review, review_id)
        return jsonify(review.to_dict())
    except Exception:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete a review object"""
    if review_id is None:
        abort(404)
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def POST_request_reviews(place_id):
    """"post request"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if not data:
        return abort(400, {'message': 'Not a JSON'})
    if 'user_id' not in data:
        abort(400)
        return abort(400, {'message': 'Missing user_id'})
    user_id = data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if 'text' not in data:
        abort(400)
        return abort(400, {'message': 'Missing text'})
    # creation of a new review
    new_review = Review(**data)
    new_review.place_id = place_id
    new_review.user_id = user_id
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def PUT_review(review_id):
    """Put request"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if not data:
        return abort(400, {'message': 'Not a JSON'})
    for key, value in data.items():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict())
