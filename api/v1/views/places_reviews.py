#!/usr/bin/python3
""" view for review object that handles restful api """
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.city import City
from models.state import State
from models.review import Review
from models.place import Place
from models import storage
from models.user import user
from models.base_model import BaseModel


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """Gets the list of all Review objects of a Place"""
    all_reviews = []  # review list
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    for review in place.reviews:  # rev = review items
        if item.place_id == place_id:
            all_reviews.append(review.to_dict())
    return jsonify(all_reviews)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def review_retrieval(review_id):
    """Retrieves review object with matching review_id """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def create_review(place_id):
    """Creates a review"""
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    user_id = body['user_id']
    if not user_id:
        abort(400, "Missing user_id")
    text = body.get('text')
    if not text:
        abort(400, "Missing text")
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    new_rev = Review(**post_content)
    new_rev.place_id = place_id
    storage.new(new_rev)
    new_rev.save()
    storage.close()
    return jsonify(new_rev.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates Review object"""
    rev = storage.get("Review", review_id)
    if review is None:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    for key, value in body.items():
        setattr(review, key, value)
    review.save()
    storage.close()
    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_review_by_id(review_id):
    """Delete a review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200
