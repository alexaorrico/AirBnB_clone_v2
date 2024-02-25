#!/usr/bin/python3
"""cities file"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def allReview(place_id):
    """list of all review objects"""
    review_list = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for review in place.reviews:
        review_list.append(review.to_dict())
    return jsonify(review_list)


@app_views.route("/reviews/<review_id>", methods=['GET'], strict_slashes=False)
def review_by_id(review_id):
    """list one review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return review.to_dict()


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def review_delete(review_id):
    """Delete a review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        review.delete()
        storage.save()
        return {}, 200


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def review_post(place_id):
    """list of all review objects"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    body = request.get_json()
    if body is None:
        abort(400, description="Not a JSON")
    if 'user_id' not in body.keys():
        abort(400, description="Missing user_id")
    user = storage.get(User, body.get('user_id'))
    if user is None:
        abort(404)
    if 'text' not in body.keys():
        abort(400, description="Missing text")
    body['place_id'] = place_id
    review = Review(**body)
    review.save()
    return review.to_dict(), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'], strict_slashes=False)
def review_put(review_id):
    """list of all review objects"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    body = request.get_json()
    if body is None:
        abort(400, description="Not a JSON")
    ignored_keys = ('id', 'user_id', 'place_id', 'created_at', 'updated_at')
    for key, value in body.items():
        if key not in ignored_keys:
            setattr(review, key, value)
    storage.save()
    return review.to_dict(), 200
