#!/usr/bin/python3
"""Create a new view for Review object that handles all default RestFul API"""


from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def review_places(place_id=None):
    """Retrieves the list of all Review objects of a Place"""
    review_pla = storage.get('Place', place_id)
    if review_pla is None:
        abort(404)
    all_review = review_pla.reviews
    list_review = []
    for rev in all_review:
        list_review.append(rev.to_dict())
    return jsonify(list_review)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def one_review(review_id=None):
    """Retrieves a Review object."""
    a_review = storage.get('Review', review_id)
    if a_review is None:
        abort(404)
    return jsonify(a_review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id=None):
    """Deletes a Review object"""
    del_review = storage.get('Review', review_id)
    if del_review is None:
        abort(404)
    storage.delete(del_review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id=None):
    """Creates a Review"""
    places = storage.get('Place', place_id)
    if places is None:
        abort(404)
    res = request.get_json()
    if res is None:
        abort(400, "Not a JSON")
    if 'user_id' not in res.keys():
        abort(400, "Missing user_id")
    id_user = storage.get('User', res['user_id'])
    if id_user is None:
        abort(404)
    if 'text' not in res.keys():
        abort(400, "Missing text")
    res['place_id'] = place_id
    newReview = Review(**res)
    storage.new(newReview)
    storage.save()
    return jsonify(newReview.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id=None):
    """Updates a Review object"""
    id_review = storage.get('Review', review_id)
    if id_review is None:
        abort(404)
    res = request.get_json()
    if res is None:
        abort(400, "Not a JSON")
    for k, v in res.items():
        if k != 'id' and k != 'created_at' and \
           k != 'updated_at' and k != 'user_id' and k != 'place_id':
            setattr(id_review, k, v)
    storage.save()
    return jsonify(id_review.to_dict()), 200
