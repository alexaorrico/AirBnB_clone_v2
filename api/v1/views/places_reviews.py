#!/usr/bin/python3
""" module that implements the review api """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def get_reviews(place_id):
    """ gets all review objects per place using the place_id """
    my_place = storage.get("Place", place_id)
    if not my_place:
        abort(404)
    return jsonify([review.to_dict() for review in my_place.reviews])


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def get_review_by_id(review_id):
    """ gets review object based on the review id """
    review = storage.get('Review', review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def deleting_review(review_id):
    """ deleting a review object using its id """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return (jsonify({})), 200


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def adding_review(place_id):
    """ adding new review to given place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    js_data = request.get_json()
    if not js_data:
        abort(400, 'Not a JSON')
    if 'user_id' not in js_data:
        return jsonify({"error": "Missing user_id"}), 400
    user_id = js_data['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if 'text' not in js_data:
        return jsonify({"error": "Missing text"}), 400
    js_data['place_id'] = place_id
    review = Review(**js_data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def updating_review(review_id):
    """updateing  a given review based on id """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    js_data = request.get_json()
    if not js_data:
        abort(400, 'Not a JSON')
    for k, v in js_data.items():
        if k not in ["id", "user_id", "place_id", "created_at",
                     "updated_at"]:
            setattr(review, k, v)
    review.save()
    return jsonify(review.to_dict()), 200
