#!/usr/bin/python3
"""comment"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, Blueprint
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """yelp"""
    lizt = []
    reviews = storage.all(Review).values()
    for review in reviews:
        if review.place_id == place_id:
            lizt.append(review.to_dict())
    return jsonify(lizt)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_a_review(review_id):
    """review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    ret = review.to_dict()
    return jsonify(ret)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_a_review(review_id):
    """ deletes review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_a_review(place_id):
    """create a state"""
    req = request.get_json()
    if not request.is_json:
        abort(400, description="Not a JSON")
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    key = 'user_id'
    if key not in req:
        abort(400, description="Missing user_id")
    key = req['user_id']
    user = storage.get(User, key)
    if user is None:
        abort(404)
    key = 'text'
    if key not in req:
        abort(400, description="Missing text")
    req['place_id'] = place_id
    new_review = Review(**req)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_a_review(review_id):
    """ this method updates a review """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    req = request.get_json()
    if not request.is_json:
        abort(400, description="Not a JSON")
    for k, value in req.items():
        if k is not "id" and k is not "created_at" and k is not "updated_at"\
           and k is not "user_id" and k is not "place_id":
            setattr(review, k, value)
    review.save()
    return jsonify(review.to_dict()), 200
