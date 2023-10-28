#!/usr/bin/python3
"""Views for Reviews"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.review import Review
from models.place import Place
from models.user import User
from flask import abort
from flask import make_response
from flask import request


@app_views.route('places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def get_reviews(place_id):
    """
    Return reviews according to its id and returns
    an error if not found
    """
    if place_id:
        dic_place = storage.get(Place, place_id)
        if dic_place is None:
            abort(404)
        else:
            reviews = storage.all(Review).values()
            list_reviews = []
            for review in reviews:
                if review.place_id == place_id:
                    list_reviews.append(review.to_dict())
            return jsonify(list_reviews)


@app_views.route('reviews/<review_id>',
                 strict_slashes=False, methods=['GET'])
def get_review(review_id):
    """Return a review based on a Place object"""
    if review_id:
        dic_review = storage.get(Review, review_id)
        if dic_review is None:
            abort(404)
        else:
            return jsonify(dic_review.to_dict())


@app_views.route('reviews/<review_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """Deletes a review if it exists, otherwise raise 404"""
    if review_id:
        review = storage.get(Review, review_id)
        if review is None:
            abort(404)
        else:
            storage.delete(review)
            storage.save()
            return make_response(jsonify({}), 200)


@app_views.route('places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def post_review(place_id):
    """Posts a review"""
    if place_id:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    reque = request.get_json()
    if "user_id" not in reque:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    user = storage.get(User, reque['user_id'])
    if user is None:
        abort(404)

    if "text" not in reque:
        return make_response(jsonify({"error": "Missing text"}), 400)
    reque['place_id'] = place_id
    reviews = Review(**reque)
    reviews.save()
    return make_response(jsonify(reviews.to_dict()), 201)


@app_views.route('reviews/<review_id>',
                 strict_slashes=False,
                 methods=['PUT'])
def update_review(review_id):
    """Updates a review"""
    if review_id:
        review_obj = storage.get(Review, review_id)
        if review_obj is None:
            abort(404)
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        reque = request.get_json()
        for key, value in reque.items():
            if key not in [
                'id',
                'user_id',
                'place_id',
                'created_at',
                    'updated_at']:
                setattr(review_obj, key, value)
        review_obj.save()
        return make_response(jsonify(review_obj.to_dict()), 200)
