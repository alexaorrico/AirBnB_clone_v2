#!/usr/bin/python3
""" Blueprint for API """

from flask import Blueprint
from models import storage
from flask import jsonify, abort, make_response,request
from models.review import Review
from models.place import Place
from models.user import User

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """ get reviews """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ get review """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """ delete review """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """ post review """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    if 'text' not in request.get_json():
        abort(400, description="Missing text")
    user = storage.get(User, request.get_json()['user_id'])
    if user is None:
        abort(404)
    review = Review(**request.get_json())
    review.place_id = place_id
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """ put review """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)

