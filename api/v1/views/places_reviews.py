#!/usr/bin/python3
""" The Review Object view
"""

from flask import jsonify, abort, request
from models.place import Place
from models.user import User
from models.review import Review
from models import storage
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_reviews(place_id):
    """ Retrieves reviews linked to a city from storage
    """
    retrieved_reviews = []
    places = storage.get(Place, place_id)
    if places:
        for review in places.reviews:
            retrieved_reviews.append(review.to_dict())
        return jsonify(retrieved_reviews), 200
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review_by_id(review_id):
    """ Retrieves one review from storage based on the id
    """
    try:
        return jsonify(storage.get(Review, review_id).to_dict()), 200
    except Exception:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review_by_id(review_id):
    """ Deletes the review from storage by its given id
    """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """ Adds a new user to storage
    """
    place = storage.get(Place, place_id)
    if place:
        body = request.get_json()
        if body is None:
            abort(400, 'Not a JSON')
        if 'text' not in body:
            abort(400, 'Missing text')
        if 'user_id' not in body:
            abort(400, 'Missing user_id')
        user_id = storage.get(User, body['user_id'])
        if user_id is None:
            abort(404)
        new_review = Review(**body)
        new_review.place_id = place_id
        new_review.save()
    else:
        abort(404)
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """ Modifies the attributes of a review if they are not dates or id
    """
    review = storage.get(Review, review_id)
    if review:
        body = request.get_json()
        if body is None:
            abort(400, 'Not a JSON')
        for key, value in body.items():
            if key not in ['id', 'user_id', 'city_id',
                           'created_at', 'updated_at']:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
    else:
        abort(404)
